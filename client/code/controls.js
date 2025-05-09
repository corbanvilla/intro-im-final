function triggerTransition() {
  resetState();
  getContent();
  playAudioWhenReady();
}

function keyPressed() {
  if (!started) {
    started = true;
    playAudioWhenReady();
  } else if (key === ' ') {
    triggerTransition();
  }
}

function mouseClicked() {
  if (!started) {
    started = true;
    playAudioWhenReady();
  } else {
    triggerTransition();
  }
}

function touchStarted() {
  if (!started) {
    started = true;
    playAudioWhenReady();
  } else {
    triggerTransition();
  }
}
