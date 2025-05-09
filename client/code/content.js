// getContent function moved from sketch.js
function getContent() {
  // Build query param for seen names
  const seenParam = seenNames.length > 0 ? `?seen=${encodeURIComponent(seenNames.join(","))}` : "";
  fetch(`/api/content${seenParam}`)
    .then(response => response.json())
    .then(data => {
      // If seen_all is true, clear the seenNames list
      if (data.seen_all) {
        seenNames = [];
      }
      // Track the name as seen
      if (data.name && !seenNames.includes(data.name)) {
        seenNames.push(data.name);
      }
      images = data.images || [];
      currentImageIndex = 0;
      imageUrl = images.length > 0 ? images[0] : null;
      if (imageUrl) {
        loadImage(imageUrl, img => {
          contentImage = img;
          renderImage();
        });
      }
      transcripts = data.transcripts;
      fetch(transcripts)
        .then(resp => resp.json())
        .then(json => {
          transcriptContent = json;
        });
      audioUrl = data.audio;
      fetch(audioUrl)
        .then(resp => resp.blob())
        .then(blob => {
          audioBlob = blob;
        });
    });
}
