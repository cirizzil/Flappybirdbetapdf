#!/usr/bin/env python3

PDF_TEMPLATE = r"""%PDF-1.6

% Root object
1 0 obj
<<
  /AcroForm << /Fields [ ###FIELD_LIST### ] >>
  /Pages 2 0 R
  /OpenAction 17 0 R
  /Type /Catalog
>>
endobj

2 0 obj
<<
  /Count 1
  /Kids [ 16 0 R ]
  /Type /Pages
>>
endobj

21 0 obj
[ ###FIELD_LIST### ]
endobj

###FIELDS###

16 0 obj
<<
  /Annots 21 0 R
  /Contents 3 0 R
  /CropBox [ 0 0 612 792 ]
  /MediaBox [ 0 0 612 792 ]
  /Parent 2 0 R
  /Resources << >>
  /Rotate 0
  /Type /Page
>>
endobj

3 0 obj
<< >>
stream
endstream
endobj

17 0 obj
<<
  /JS 42 0 R
  /S /JavaScript
>>
endobj

42 0 obj
<< >>
stream
/*
  Flappy Bird in PDF - Button-Click Version

  - "Start" button => begins game or resets.
  - "FLAP" button => sets birdVel upward (birdVel = flapStrength).
  - Gravity pulls bird down.
  - Pipes move left; collision ends game.

  Only works in Adobe Acrobat (desktop). Most other PDF
  readers don't support PDF JavaScript or form fields at this level.
*/

// Minimal 'setInterval' polyfill for Acrobat
function setIntervalPolyfill(cb, ms) {
    var codeStr = "(" + cb.toString() + ")();";
    return app.setInterval(codeStr, ms);
}
function clearIntervalPolyfill(id) {
    app.clearInterval(id);
}

var seed = Date.now() % 2147483647;
function rand() {
    seed = (seed * 16807) % 2147483647;
    return seed;
}

// Pixel grid references
var pixel_fields = [];
var timerId = null;

// Grid settings
var GRID_WIDTH  = ###GRID_WIDTH###;
var GRID_HEIGHT = ###GRID_HEIGHT###;

// Bird
var birdX = 5;
var birdY = 10;
var birdVel = 0;
// Gravity is subtracted from birdVel => bird falls
var gravity = 0.6;
// Flap => sets birdVel = flapStrength => upward movement
var flapStrength = 2.5;

// Pipes
var pipes = [];
var pipeGap = 4;      
var pipeSpacing = 18; 
var pipeSpeed = 1;    

// Score
var score = 0;
var gameRunning = false;

// Just show/hide
// (If you want different colors, you need more complicated appearance objects.)
function set_pixel(x, y, visible) {
    if (x < 0 || y < 0 || x >= GRID_WIDTH || y >= GRID_HEIGHT) return;
    var f = pixel_fields[x][y];
    if (!f) return;
    f.hidden = !visible;
}

// Clears everything to "hidden" (background)
function clear_field() {
    for (var x = 0; x < GRID_WIDTH; x++) {
        for (var y = 0; y < GRID_HEIGHT; y++) {
            set_pixel(x, y, false);
        }
    }
}

// Spawns a new pipe on the right
function spawnPipe() {
    var gapY = 3 + (rand() % (GRID_HEIGHT - pipeGap - 6));
    pipes.push({
        x: GRID_WIDTH,
        gapY: gapY
    });
}

// The user clicks "FLAP" => do_flap is called
function do_flap() {
    birdVel = flapStrength;
}

// Called every frame if game is running
function update_game() {
    // Bird falls (velocity goes down)
    birdVel -= gravity;
    birdY += birdVel;

    // Move pipes left
    for (var i = 0; i < pipes.length; i++) {
        pipes[i].x -= pipeSpeed;
    }
    // Remove off-screen => +1 score
    while (pipes.length > 0 && pipes[0].x < -1) {
        pipes.shift();
        score++;
        update_score();
    }
    // Spawn new pipe if needed
    if (pipes.length == 0) {
        spawnPipe();
    } else {
        var lastPipe = pipes[pipes.length - 1];
        if (lastPipe.x < GRID_WIDTH - pipeSpacing) {
            spawnPipe();
        }
    }
    // Check out of bounds => game over
    if (birdY < 0 || birdY >= GRID_HEIGHT) {
        end_game();
        return;
    }
    // Check collisions at birdX
    var bY = Math.floor(birdY);
    for (var j = 0; j < pipes.length; j++) {
        var px = Math.floor(pipes[j].x);
        if (px == birdX) {
            var gTop = pipes[j].gapY;
            var gBot = gTop + pipeGap - 1;
            if (bY < gTop || bY > gBot) {
                end_game();
                return;
            }
        }
    }
}

// Draw the scene
function draw_scene() {
    clear_field();
    // Draw pipes
    for (var i = 0; i < pipes.length; i++) {
        var px = Math.floor(pipes[i].x);
        if (px >= 0 && px < GRID_WIDTH) {
            var gTop = pipes[i].gapY;
            var gBot = gTop + pipeGap - 1;
            for (var row = 0; row < GRID_HEIGHT; row++) {
                if (row < gTop || row > gBot) {
                    set_pixel(px, row, true); // show pipe
                }
            }
        }
    }
    // Draw bird
    var bX = birdX;
    var bY = Math.floor(birdY);
    set_pixel(bX, bY, true);
}

// The main loop
function game_tick() {
    if (!gameRunning) return;
    update_game();
    draw_scene();
}

// Start or reset
function start_game() {
    pipes = [];
    birdY = 10;
    birdVel = 0;
    score = 0;
    update_score();
    clear_field();
    spawnPipe();
    gameRunning = true;
    if (timerId) {
        clearIntervalPolyfill(timerId);
    }
    timerId = setIntervalPolyfill(game_tick, 100);
}

// End game
function end_game() {
    gameRunning = false;
    clearIntervalPolyfill(timerId);
    app.alert("Game Over! Final Score: " + score);
}

function update_score() {
    this.getField("T_score").value = "Score: " + score;
}

// Called once when PDF is opened
function flappy_init() {
    // Gather references to pixel fields
    for (var x = 0; x < GRID_WIDTH; x++) {
        pixel_fields[x] = [];
        for (var y = 0; y < GRID_HEIGHT; y++) {
            pixel_fields[x][y] = this.getField("P_" + x + "_" + y);
        }
    }
    app.execMenuItem("FitPage");
}

flappy_init();

endstream
endobj

18 0 obj
<<
  /JS 43 0 R
  /S /JavaScript
>>
endobj

43 0 obj
<< >>
stream

endstream
endobj

trailer
<<
  /Root 1 0 R
>>
%%EOF
"""

PIXEL_OBJ = r"""
###IDX### obj
<<
  /FT /Btn
  /Ff 1
  /MK <<
    /BG [ 0.8 ]
    /BC [ 0.5 0.5 0.5 ]
  >>
  /Border [ 0 0 1 ]
  /P 16 0 R
  /Rect [ ###RECT### ]
  /Subtype /Widget
  /T (P_###X###_###Y###)
  /Type /Annot
>>
endobj
"""

BUTTON_AP_STREAM = r"""
###IDX### obj
<<
  /BBox [ 0 0 ###WIDTH### ###HEIGHT### ]
  /FormType 1
  /Matrix [1 0 0 1 0 0]
  /Resources <<
    /Font <<
      /HeBo 10 0 R
    >>
    /ProcSet [ /PDF /Text ]
  >>
  /Subtype /Form
  /Type /XObject
>>
stream
q
0.75 g
0 0 ###WIDTH### ###HEIGHT### re
f
Q
BT
/HeBo 12 Tf
0 g
10 8 Td
(###TEXT###) Tj
ET
endstream
endobj
"""

BUTTON_OBJ = r"""
###IDX### obj
<<
  /A <<
    /JS ###SCRIPT_IDX### R
    /S /JavaScript
  >>
  /AP <<
    /N ###AP_IDX### R
  >>
  /F 4
  /FT /Btn
  /Ff 65536
  /MK <<
    /BG [0.75]
    /CA (###LABEL###)
  >>
  /P 16 0 R
  /Rect [ ###RECT### ]
  /Subtype /Widget
  /T (###NAME###)
  /Type /Annot
>>
endobj
"""

TEXT_OBJ = r"""
###IDX### obj
<<
  /FT /Tx
  /Ff 0
  /P 16 0 R
  /Rect [ ###RECT### ]
  /Subtype /Widget
  /T (###NAME###)
  /V (###LABEL###)
  /Type /Annot
>>
endobj
"""

STREAM_OBJ = r"""
###IDX### obj
<< >>
stream
###CONTENT###
endstream
endobj
"""

#####################################################################
# Python Script
#####################################################################
PX_SIZE = 12
GRID_WIDTH = 30
GRID_HEIGHT= 20
OFFSET_X = 100
OFFSET_Y = 100

fields_text = ""
field_indexes= []
obj_idx = 50

def add_field(field_str: str):
    global fields_text, field_indexes, obj_idx
    fields_text += field_str
    field_indexes.append(obj_idx)
    obj_idx += 1

# 1) Create the pixel buttons
for x in range(GRID_WIDTH):
    for y in range(GRID_HEIGHT):
        rect_left   = OFFSET_X + x * PX_SIZE
        rect_bottom = OFFSET_Y + y * PX_SIZE
        rect_right  = rect_left + PX_SIZE
        rect_top    = rect_bottom + PX_SIZE

        pix = PIXEL_OBJ
        pix = pix.replace("###IDX###", f"{obj_idx} 0")
        pix = pix.replace("###RECT###", f"{rect_left} {rect_bottom} {rect_right} {rect_top}")
        pix = pix.replace("###X###", str(x))
        pix = pix.replace("###Y###", str(y))
        add_field(pix)

def add_button(label, name, x, y, w, h, js_code):
    """
    Creates a PDF button with:
    1) A JavaScript object
    2) An appearance stream
    3) The actual button referencing them
    """
    global obj_idx

    # 1) JS object
    script_obj = STREAM_OBJ
    script_obj = script_obj.replace("###IDX###", f"{obj_idx} 0")
    script_obj = script_obj.replace("###CONTENT###", js_code)
    add_field(script_obj)

    # 2) Appearance stream
    ap_obj_idx = obj_idx
    ap_stream = BUTTON_AP_STREAM
    ap_stream = ap_stream.replace("###IDX###", f"{ap_obj_idx} 0")
    ap_stream = ap_stream.replace("###WIDTH###", str(w))
    ap_stream = ap_stream.replace("###HEIGHT###", str(h))
    ap_stream = ap_stream.replace("###TEXT###", label)
    add_field(ap_stream)

    # 3) The button object
    btn_obj_idx = obj_idx
    btn = BUTTON_OBJ
    btn = btn.replace("###IDX###", f"{btn_obj_idx} 0")
    # The *first* of these new objects is the JS script => ap_obj_idx-1
    # The *second* is the appearance => ap_obj_idx
    btn = btn.replace("###SCRIPT_IDX###", f"{ap_obj_idx-1} 0")
    btn = btn.replace("###AP_IDX###", f"{ap_obj_idx} 0")
    btn = btn.replace("###LABEL###", label)
    btn = btn.replace("###NAME###", name)
    btn = btn.replace("###RECT###", f"{x} {y} {x+w} {y+h}")
    add_field(btn)

def add_textfield(label, name, x, y, w, h):
    """
    Simple text field to display the score
    """
    global obj_idx

    txt = TEXT_OBJ
    txt = txt.replace("###IDX###", f"{obj_idx} 0")
    txt = txt.replace("###LABEL###", label)
    txt = txt.replace("###NAME###", name)
    txt = txt.replace("###RECT###", f"{x} {y} {x+w} {y+h}")
    add_field(txt)

# 2) Add "Start" button in the center
start_x = OFFSET_X + (GRID_WIDTH * PX_SIZE)//2 - 30
start_y = OFFSET_Y + (GRID_HEIGHT * PX_SIZE)//2 - 15
add_button(
    label="Start",
    name="B_start",
    x=start_x,
    y=start_y,
    w=60,
    h=30,
    js_code="start_game();"
)

# 3) Add "Flap" button to let the bird jump
flap_x = OFFSET_X + GRID_WIDTH*PX_SIZE + 20
flap_y = OFFSET_Y + (GRID_HEIGHT*PX_SIZE)//2 - 15
add_button(
    label="FLAP",
    name="B_flap",
    x=flap_x,
    y=flap_y,
    w=60,
    h=30,
    js_code="do_flap();"
)

# 4) Score display
score_x = OFFSET_X + GRID_WIDTH*PX_SIZE + 10
score_y = OFFSET_Y + GRID_HEIGHT*PX_SIZE - 30
add_textfield("Score: 0", "T_score", score_x, score_y, 80, 20)

# Insert into template
pdf_text = PDF_TEMPLATE
pdf_text = pdf_text.replace("###FIELDS###", fields_text)
pdf_text = pdf_text.replace("###FIELD_LIST###",
    " ".join([f"{idx} 0 R" for idx in field_indexes])
)
pdf_text = pdf_text.replace("###GRID_WIDTH###", str(GRID_WIDTH))
pdf_text = pdf_text.replace("###GRID_HEIGHT###", str(GRID_HEIGHT))

# Write out
with open("flappy_out.pdf", "wb") as f:
    f.write(pdf_text.encode("utf-8", "replace"))

print("Created flappy_out.pdf! Open in Adobe Acrobat (desktop) to click 'Start' and 'FLAP'.")
