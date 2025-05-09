let ws;
let contentImage = null;
let imageUrl = null;
let interFont;
let transcripts = null;
let audioUrl = null;
let transcriptContent = null;
let audioBlob = null;
let started = false;

// Global list to track multiple Textbox instances
let textboxes = [];

// Track seen names
let seenNames = [];

// Track images and switching logic
let images = [];
let currentImageIndex = 0;
let imageSwitchInterval = 0;
let audioDuration = 0;

// Replace switch1Active with isPaused
let isPaused = false;

function preload() {
  getContent();
  interFont = loadFont('assets/fonts/static/Inter_24pt-ExtraLight.ttf',
    () => console.log('Inter ExtraLight font loaded:', interFont),
    (err) => console.error('Error loading Inter ExtraLight font:', err)
  );
}

function setup() {
  createCanvas(windowWidth, windowHeight);
  background(0);
  ws = new WebSocket('/api/controls');
  ws.onmessage = function(event) {
    // Parse JSON and set audio volume and playback speed
    console.log('WebSocket message:', event.data);
    let data;
    try {
      data = JSON.parse(event.data);
    } catch (e) {
      console.error('Error parsing ws message:', e, event.data);
      return;
    }
    // Handle switch1: pause/unpause audio and update isPaused
    isPaused = !!data.switch1;
    if (window.audio) {
      // Switch pause state
      if (isPaused && !window.audio.paused) {
        window.audio.pause();
      } else if (!isPaused && window.audio.paused && started) {
        window.audio.play();
      }
      // Arduino volume is 0-255, map to 0.0-1.0 for HTML audio
      window.audio.volume = constrain(data.pot2 / 255, 0, 1);
      // Arduino pot2 is 0-255, map to 0.75-3.0 for playback speed
      window.audio.playbackRate = map(data.pot3, 0, 255, 0.75, 3.0);
    }
    // Call triggerTransition if button1 or button2 is pressed
    if (data.button1 || data.button2) {
      triggerTransition();
    }
  };

  let checkAudioLoaded = setInterval(() => {
    if (audioBlob) {
      const audioUrlObj = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrlObj);
      audio.onloadedmetadata = () => {
        audioDuration = audio.duration;
        if (images.length > 0) {
          imageSwitchInterval = audioDuration / images.length;
        } else {
          imageSwitchInterval = 0;
        }
      };
      clearInterval(checkAudioLoaded);
    }
  }, 100);
}

function draw() {
  if (!started) {
    background(0);
    fill(255);
    textAlign(CENTER, CENTER);
    textSize(48);
    text('click to start', width / 2, height / 2);
    return;
  }

  // Blackout and show message if isPaused
  if (isPaused) {
    background(0);
    fill(255);
    textAlign(CENTER, CENTER);
    textSize(48);
    text('flip the red button to start', width / 2, height / 2);
    return;
  }

  // Image switching logic based on audio time
  if (window.audio && images.length > 1 && audioDuration > 0) {
    let idx = Math.floor(window.audio.currentTime / (audioDuration / images.length));
    idx = Math.min(idx, images.length - 1);
    if (idx !== currentImageIndex) {
      currentImageIndex = idx;
      imageUrl = images[currentImageIndex];
      loadImage(imageUrl, img => {
        contentImage = img;
        renderImage();
      });
    }
  }

  renderImage();

  // Add textboxes based on audio playback and transcript timing
  if (window.audio && transcriptContent && transcriptContent.length > 0) {
    while (transcriptContent.length > 0) {
      const el = transcriptContent[0];
      if (window.audio.currentTime > el.audio_offset) {
        if (el.boundary_type === 'SpeechSynthesisBoundaryType.Punctuation') {
          transcriptContent.shift();
          continue;
        }
        if (el.is_stopword === true) {
          transcriptContent.shift();
          continue;
        }
        let scalar = random(0.35, 1.5);
        textboxes.push(new Textbox(el.text, interFont, scalar));
        transcriptContent.shift(); // Remove processed element
      } else {
        break;
      }
    }
  }

  for (let i = textboxes.length - 1; i >= 0; i--) {
    let tb = textboxes[i];
    tb.draw();
    tb.decay();
    if (tb.opacity === 0) {
      textboxes.splice(i, 1);
    }
  }
}

// Consolidated reset logic
function resetState() {
  // Stop and clear audio
  if (window.audio) {
    window.audio.pause();
    window.audio.currentTime = 0;
    window.audio = null;
  }
  // Clear textboxes and transcript
  textboxes = [];
  transcriptContent = null;
  audioBlob = null;

  images = [];
  currentImageIndex = 0;
  imageSwitchInterval = 0;
  audioDuration = 0;
}
