function playAudioWhenReady() {
  if (audioBlob) {
    const audioUrlObj = URL.createObjectURL(audioBlob);
    window.audio = new Audio(audioUrlObj);
    window.audio.onloadedmetadata = () => {
      audioDuration = window.audio.duration;
      if (images.length > 0) {
        imageSwitchInterval = audioDuration / images.length;
      } else {
        imageSwitchInterval = 0;
      }
    };
    window.audio.play();
    window.audio.onended = () => {
      resetState();
      getContent();
      playAudioWhenReady();
    };
  } else {
    setTimeout(playAudioWhenReady, 100);
  }
}