// Textbox class with black background, white text, and minimally rounded corners
class Textbox {
  // scalar: a single value that controls overall size
  constructor(text, font, scalar) {
    // Calculate box and text size based on scalar
    // scalar ~1.0 is default, <1 smaller, >1 larger
    this.w = 220 * scalar;
    this.h = 50 * scalar;
    this.textSize = 16 + 32 * scalar; // Make font size scale more dramatically
    this.text = text;
    this.font = font;
    this.radius = 8 * scalar; // scale rounding too
    this.opacity = 255;

    // Padding from canvas edges
    const edgePadding = 40 * scalar;
    // Randomize position so box stays within canvas and doesn't run off
    this.x = random(edgePadding, width - this.w - edgePadding);
    this.y = random(edgePadding, height - this.h - edgePadding);
  }

  draw() {
    if (this.opacity <= 0) return;
    push();
    fill(0, this.opacity);
    noStroke();
    rect(this.x, this.y, this.w, this.h, this.radius);

    if (this.font) {
      textFont(this.font);
      textStyle(NORMAL);
    }
    let padding = 10 * (this.w / 220); // scale padding with box size
    let maxTextWidth = this.w - padding * 2;
    let ts = this.textSize;
    textSize(ts);
    textAlign(CENTER, CENTER);
    // Shrink text size if needed to fit
    while (textWidth(this.text) > maxTextWidth && ts > 8) {
      ts--;
      textSize(ts);
    }
    // Adjust vertical alignment
    let yOffset = this.h * 0.1;
    fill(255, this.opacity);
    text(this.text, this.x + this.w / 2, this.y + this.h / 2 - yOffset);
    pop();
  }

  decay() {
    this.opacity = max(0, this.opacity - 1);
  }
}
