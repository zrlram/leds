import model
from sphere_pixel import *

def ring():
        millis = int(round(time.time() * 1000))

        for pixel in range(numLEDs + 1):
            t = i * 0.2 + millis * 0.002
            red = int(128 + 96 * sin(t))
            green = int(128 + 96 * sin(t + 0.1))
            blue = int(128 + 96 * sin(t + 0.3))
            model.set_pixels( 
            if pixel >= numLEDs: break
            pixels[pixel] = (red, green, blue)
            pixel += 1 

        draw()

function draw() {
    var millis = new Date().getTime();

    for (var pixel = 0; pixel < 512; pixel++)
    {
        var t = pixel * 0.2 + millis * 0.002;
        var red = 128 + 96 * Math.sin(t);
        var green = 128 + 96 * Math.sin(t + 0.1);
        var blue = 128 + 96 * Math.sin(t + 0.3);

        client.setPixel(pixel, red, green, blue);
    }
    client.writePixels();
}

setInterval(draw, 30);
