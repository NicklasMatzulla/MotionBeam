/*
 * Copyright (c) 2024 Nicklas Matzulla
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

function initSections(numSectionsX, numSectionsY) {
  var canvas = document.getElementById("camera_preview");
  var ctx = canvas.getContext("2d");

  canvas.addEventListener('click', function(event) {
    var x = event.offsetX;
    var y = event.offsetY;
    var sectionX = Math.floor(x / (canvas.width / numSectionsX));
    var sectionY = Math.floor(y / (canvas.height / numSectionsY));
    toggleSection(sectionX, sectionY);
  });

  function drawFrame(frame) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(frame, 0, 0, canvas.width, canvas.height);
  }

  function getCameraFrame() {
    var frame = new Image();
    frame.src = 'http://127.0.0.1:80/video_feed';
    frame.onload = function() {
      drawFrame(frame);
    }
  }

  setInterval(getCameraFrame, 50);

  function toggleSection(x, y) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/toggle_section", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send("x=" + x + "&y=" + y);
  }
}