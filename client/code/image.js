function renderImage() {
  if (!window._renderer) return; // Prevent drawing before canvas exists
  if (contentImage) {
    background(0);
    // Calculate scale to fill the screen, cropping as needed
    let imgAspect = contentImage.width / contentImage.height;
    let canvasAspect = width / height;
    let drawWidth, drawHeight;

    if (imgAspect > canvasAspect) {
      drawHeight = height;
      drawWidth = imgAspect * height;
    } else {
      drawWidth = width;
      drawHeight = width / imgAspect;
    }

    image(
      contentImage,
      (width - drawWidth) / 2,
      (height - drawHeight) / 2,
      drawWidth,
      drawHeight
    );
  }
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
  renderImage();
}