from cmu_112_graphics import *
from initializer import *
import numpy, math, random, time

def initEditor(app):
    # Rectangular buttons
    width = 0.12 * app.width
    height = 0.5 * width
    app.space = ((app.height-app.width*9/16)/2-height*2)/3
    leftAlign = mar = spacing = app.space
    rightAlign = app.width - leftAlign
    app.editTitle = Button('TITLE', leftAlign, mar, leftAlign+width, mar+height)
    app.editColor = Button('COLOR', leftAlign, mar+height+spacing, 
                    leftAlign+width, mar+height*2+spacing)
    app.editBackground = Button('BACKGROUND', leftAlign+width+spacing, mar,
                                leftAlign+width+0.17*app.width+spacing, 
                                mar+height)
    app.moveTitle = Button('MOVE TITLE', leftAlign+width+spacing, 
                            mar+height+spacing, 
                            leftAlign+width+0.17*app.width+spacing, 
                            mar+height*2+spacing)
    app.reset = Button('RESET', rightAlign-width, mar+height+spacing,
                       rightAlign, mar+height*2+spacing)
    app.toggleMenu = Button('HIDE MENU', rightAlign-0.15*app.width, mar,
                     rightAlign, mar+height)
    app.next = Button('NEXT', rightAlign-width, app.height-mar-height,
                      rightAlign, app.height-mar)
    app.back = Button('BACK', leftAlign, app.height-mar-height, leftAlign+width,
                      app.height-mar)
    app.showMenu = True
    # Round buttons
    d = 30 # diameter
    app.zoomIn = Button('+', leftAlign, app.height-mar-spacing-2*d, leftAlign+d,
                        app.height-mar-spacing-d)
    app.zoomOut = Button('-', leftAlign, app.height-mar-d, leftAlign+d,
                         app.height-mar)

def initImageEditor(app):
    width = 0.12 * app.width
    height = 0.5 * width
    leftAlign = mar = spacing = app.space
    rightAlign = app.width - leftAlign
    app.upload = Button('UPLOAD IMAGE', 0.35*app.width, 0.45*app.height,
                        0.65*app.width, 0.55*app.height)
    app.brighten = Button('BRIGHTEN', leftAlign, mar, leftAlign+width, mar+height)
    app.darken = Button('DARKEN', leftAlign, mar+height+spacing, 
                        leftAlign+width, mar+height*2+spacing)
    app.contrastUp = Button('CONTRAST(+)', leftAlign+width+spacing, mar,
                            leftAlign+width+0.17*app.width+spacing, 
                            mar+height)
    app.contrastDown = Button('CONTRAST(-)', leftAlign+width+spacing, 
                              mar+height+spacing, 
                              leftAlign+width+0.17*app.width+spacing, 
                              mar+height*2+spacing)
    app.blur = Button('BLUR', leftAlign+width+0.17*app.width+spacing*2, mar,
                      leftAlign+0.17*app.width+width*2+spacing, mar+height)

def initEffects(app):
    app.pColor = '#ffffff'
    app.anyColor = False
    app.particles = []
    app.t0 = time.time()
    # saving
    app.framet0 = None
    app.record = False
    app.takeShots = False
    app.path = None
    app.frameCt = 0
    app.bbox = getBbox(app)
    # glowTrailMode
    app.temp = []
    app.trail = []
    app.showTrail = None
    # smokeMode
    app.growSmoke = False
    app.smokeX, app.smokeY = None, None
    # fireworksMode
    app.growFireworks = False
    app.fireX, app.fireY = None, None
    app.seed = None
    app.v0 = None
    app.grav = 500
    app.exploded = None
    # buttons
    width = 0.4 * app.width
    height = 0.15 * width
    top = 0.4 * app.height
    spacing = 0.05 * app.width
    app.glowTrail = Button('GLOW TRAIL', app.width/2-width/2, top, 
                           app.width/2+width/2, top+height)
    app.smoke = Button('SMOKE', app.width/2-width/2, top+height+spacing,
                       app.width/2+width/2, top+height*2+spacing)
    app.fireworks = Button('FIREWORKS', app.width/2-width/2, 
                           top+height*2+spacing*2, app.width/2+width/2, 
                           top+height*3+spacing*2)
    app.eColor = Button('COLOR', app.editTitle.x0, app.editTitle.y0,
                        app.editTitle.x1, app.editTitle.y1)
    app.randColor = Button('RANDOM COLOR', app.toggleMenu.x0-app.width*0.05, 
                           app.toggleMenu.y0, app.toggleMenu.x1, 
                           app.toggleMenu.y1)

#################################################
# Welcome Mode
#################################################

def welcomeMode_mousePressed(app, event):
    title = app.getUserInput('Enter your video title:')
    if not title == None:
        app.mode = 'editMode'
        initEditor(app)
        initCamera(app)
        app.lines = []
        updateTitle(app, title)

def welcomeScreen(app):
    app.location = [-6.0, 3.0, 5.0]
    app.lookAt = [0.0, 0.0, 0.0]
    app.x0, app.y0, app.x1, app.y1 = -50, -50, 50, 50
    updateTitle(app, '3D VIDEO TITLE GENERATOR')

#################################################
# Edit Mode
#################################################

def editMode_keyPressed(app, event):
    if event.key == "Left": app.location[0] -= 1
    elif event.key == "Right": app.location[0] += 1
    elif event.key == "Down": app.location[1] -= 1
    elif event.key == "Up": app.location[1] += 1
    elif event.key in "sS": app.location[2] -= 1
    elif event.key in "wW": app.location[2] += 1
    elif event.key == 'r':
        app.mode = 'effectsMode'
        initEffects(app)
        app.t0 = time.time()
    if event.key in "wsWS" or event.key in ("Left", "Right", "Up", "Down"):
        updateView(app)

def editMode_mousePressed(app, event):
    x, y = event.x, event.y
    if isClicked(app.editTitle, x, y):
        title = app.getUserInput('Change title to:')
        if not title == None: 
            updateTitle(app, title)
    elif isClicked(app.editColor, x, y):
        color = askForColor(app)
        if color != None:
            app.titleColor = color
    elif isClicked(app.editBackground, x, y):
        app.mode = 'backgroundMode'
        initImageEditor(app)
    elif isClicked(app.moveTitle, x, y):
        app.mode = 'moveTitleMode'
    elif isClicked(app.toggleMenu, x, y):
        app.showMenu = not app.showMenu
        if app.showMenu == True:
            app.toggleMenu.name = 'HIDE MENU'
        else:
            app.toggleMenu.name = 'SHOW MENU' 
    elif isClicked(app.zoomIn, x, y):
        zoomInOrOut(app, +1)
        if app.minFOV == True: app.minFOV = False
        if app.x0 > -8: # max FOV reached, zoom out
            zoomInOrOut(app, -1)
            app.maxFOV = True
        updateView(app)
    elif isClicked(app.zoomOut, x, y):
        zoomInOrOut(app, -1)
        if app.maxFOV == True: app.maxFOV = False
        if app.x0 < -50: # min FOV reached, zoom in
            zoomInOrOut(app, +1)
            app.minFOV = True    
        updateView(app) 
    elif isClicked(app.reset, x, y):
        initCamera(app)
        app.uploaded = None
        app.titleColor = 'white'
        app.transX, app.transY = 0, 0
        updateView(app) 
    elif isClicked(app.next, x, y):
        initEffects(app)
        app.mode = 'effectsMode'
        app.t0 = time.time()

def updateTitle(app, title): # convert title string to corner coordinates
    temp = []
    for c in title:
        for char in app.characters:
            if char.name == c.upper():
                temp.append(char.corners)
                break
    app.title = temp
    updateView(app)

def updateView(app):
    makeProjection(app)
    # Store all the points to be connected for the title in app.lines
    lines = []
    for i in range(len(app.title)):
        corners = app.title[i]
        if corners != [(0,0),(5,0)]:
            lines.append(charLines(app, 1, corners, i)) # default depth=1
    # In the end, app.lines will be:
    # [ [points in first character], ..., [points in last character] ]
    app.lines = lines

def charLines(app, depth, corners, index):
    # Get the x-position of this character in space
    # By default, the middle of the title will always be at the center
    charSpacing = 1
    dist = len(app.title) // 2 - index
    if len(app.title) % 2 == 1:
        startX = dist * (charSpacing + 5)
    else:
        startX = (dist - 0.5) * (charSpacing + 5)
    # Get all the points to be connected for this character
    # Store them as points on two parallel planes
    linePoints = []
    center = app.charCenter + (depth/2,)
    for z in [0, depth]: # slightly based on W4 spicy recitation
        planePoints = []
        for x, y in corners:
            worldX = startX - (x - center[0]) # x-axis points to the left
            worldY = y - center[1]
            worldZ = z - center[2]
            worldPoint = (worldX, worldY, worldZ)
            cameraX, cameraY = project(app, worldPoint)
            planePoints.append((cameraX+app.transX, cameraY+app.transY))
        linePoints.append(planePoints)
    # In the end, linePoints will be:
    # [ [points on planeA], [points on planeB] ]
    return linePoints

def zoomInOrOut(app, k):
    d = 3 # change of FOV upon each click
    app.x0 += k*d
    app.y0 += k*d
    app.x1 -= k*d
    app.y1 -= k*d

def distance(x0, y0, x1, y1):
    return ( (x1 - x0)**2 + (y1 - y0)**2 ) ** 0.5

#################################################
# Background Mode
#################################################

def backgroundMode_mousePressed(app, event):
    x, y = event.x, event.y
    if app.uploaded:
        if isClicked(app.next, x, y): # displayed as 'OK'
            app.mode = 'editMode'
        elif isClicked(app.brighten, x, y):
            adjustBrightness(app, +5)
        elif isClicked(app.darken, x, y):
            adjustBrightness(app, -5)
        elif isClicked(app.contrastUp, x, y):
            adjustContrast(app, 1.15)
        elif isClicked(app.contrastDown, x, y):
            adjustContrast(app, 0.85)
        elif isClicked(app.blur, x, y):
            blurImage(app, 3)
        elif isClicked(app.reset, x, y):
            app.background = copy.copy(app.tempIm)
        elif isClicked(app.back, x, y):
            app.uploaded = False
    else:
        if isClicked(app.upload, x, y):
            image = app.loadImage()
            if image != None:
                imageWidth, imageHeight = image.size
                ratio = (app.width * 9 / 16) / imageHeight
                app.tempIm = app.scaleImage(image, ratio)
                app.background = app.scaleImage(image, ratio)
                app.uploaded = True
        elif isClicked(app.back, x, y):
            app.mode = 'editMode'

# Reference:
# https://www.youtube.com/watch?v=4ifdUQmZqhM&t=1040s
def adjustBrightness(app, dBri):
    # change brightness by adding a value to each RGB channel of each pixel
    for x in range(app.background.width):
        for y in range(app.background.height):
            pixel = app.background.getpixel((x,y))
            r,g,b = pixel[0], pixel[1], pixel[2]
            if (0<=r+dBri<=255) and (0<=g+dBri<=255) and (0<=b+dBri<=255):
                app.background.putpixel((x,y),(r+dBri,g+dBri,b+dBri))

def blurImage(app, radius):
    # blur an image by assigning the average RGB value of the neighbors of
    # each pixel
    nbrLen = radius // 2 # radius is the side length of the neighbor box
    for x in range(app.background.width):
        for y in range(app.background.height):
            avgR = int(totalColor(app, x, y, nbrLen)[0] / (radius**2))
            avgG = int(totalColor(app, x, y, nbrLen)[1] / (radius**2))
            avgB = int(totalColor(app, x, y, nbrLen)[2] / (radius**2))
            if (0<=avgR<=255) and (0<=avgG<=255) and (0<=avgB<=255):
                app.background.putpixel((x,y), (avgR, avgG, avgB))

def totalColor(app, x, y, nbrLen):
    # get the sum of the neighbor pixels' RGB values
    total = [0, 0, 0]
    maxX, maxY = app.background.width, app.background.height
    for nbrX in range(max(0, x-nbrLen), min(maxX-1, x+nbrLen) + 1):
        for nbrY in range(max(0, y-nbrLen), min(maxY-1, y+nbrLen) + 1):
            pixel = app.background.getpixel((nbrX, nbrY))
            nbrR, nbrG, nbrB = pixel[0], pixel[1], pixel[2]
            total[0] += nbrR
            total[1] += nbrG
            total[2] += nbrB
    return total

# Reference:
# https://ie.nitk.ac.in/blog/2020/01/19/algorithms-for-adjusting-brightness-and-contrast-of-an-image/
def adjustContrast(app, factor):
    # change contrast by changing the distance of each RGB channel with a
    # mid point (R = G = B = 128)
    for x in range(app.background.width):
        for y in range(app.background.height):
            pixel = app.background.getpixel((x,y))
            r = factor * (pixel[0] - 128 ) + 128
            g = factor * (pixel[1] - 128 ) + 128
            b = factor * (pixel[2] - 128 ) + 128
            if (0<=r<=255) and (0<=g<=255) and (0<=b<=255):
                app.background.putpixel((x,y),(int(r),int(g),int(b)))

#################################################
# Move Title Mode
#################################################

def moveTitleMode_mouseDragged(app, event):
    x, y = event.x, event.y
    if app.top < y < app.bottom:
        app.transX, app.transY = x - app.width/2, y - app.height/2
        updateView(app)

def moveTitleMode_keyPressed(app, event):
    if event.key == 'Up': app.transY -= 10
    elif event.key == 'Down': app.transY += 10
    elif event.key == 'Left': app.transX -= 10
    elif event.key == 'Right': app.transX += 10
    if event.key in 'UpDownLeftRight': updateView(app)

def moveTitleMode_mousePressed(app, event):
    x, y = event.x, event.y
    if isClicked(app.back, x, y): # displayed as 'RESET'
        app.transX, app.transY = 0, 0
        updateView(app)
    elif isClicked(app.next, x, y): # displayed as 'OK'
        app.mode = 'editMode'

#################################################
# Effects Mode
#################################################

def effectsMode_mousePressed(app, event):
    x, y = event.x, event.y
    if isClicked(app.glowTrail, x, y):
        app.mode = 'glowTrailMode'
        app.particles = []
    elif isClicked(app.smoke, x, y):
        app.mode = 'smokeMode'
        app.particles = []
        app.growSmoke = False
    elif isClicked(app.fireworks, x, y):
        app.mode = 'fireworksMode'
        app.particles = []
    elif isClicked(app.back, x, y):
        app.mode = 'editMode'

def effectsMode_timerFired(app):
    if len(app.particles) < 40 and time.time() - app.t0 >= 0.01:
        theta = random.randint(0, 6283) / 1000
        r = random.randint(app.width // 3, app.width // 3 + 2)
        cx = app.width / 2 + r * math.cos(theta)
        cy = app.height / 2 + r * math.sin(theta)
        vx, vy = random.randint(-15, 15) / 10, random.randint(-15, 15) / 10
        color = randomColor()
        p = Particle(cx, cy, vx, vy, time.time(), color)
        app.particles.append(p)
        app.t0 = time.time()
    emitParticles(app.particles, 1.5)

def emitParticles(pList, lifespan):
    for particle in pList:
        particle.cx += particle.vx
        particle.cy += particle.vy
        # Trail fades out
        particle.alpha -= 0.01
        if particle.alpha >= 0:
            (r, g, b) = getAlphaColor(particle.color, particle.alpha)
            particle.color = rgbString(r, g, b)
        # Particle dies after lifespan
        if time.time() - particle.birth >= lifespan:
            pList.remove(particle)

#################################################
# Glow Trail Mode
#################################################

def glowTrailMode_timerFired(app):
    if app.particles != []:
        emitParticles(app.particles, 1)
        if app.particles == []: 
            app.showTrail = True
    elif app.showTrail:
        if app.trail == []:
            loopTrail(app, copy.deepcopy(app.temp), time.time())
        else:
            emitParticles(app.trail, 1)
    if app.takeShots: # Save snapshots of the frame
        path = app.path
        if (path):
            i = app.frameCt
            if i < app.maxFrames and time.time() - app.framet0 >= 0.05:
                if (not path.endswith('.png')): path += '.png'
                path = path.replace('.png', f'{i}.png')
                result = ImageGrabber.grab((app.bbox))
                result.save(path)
                path = path.replace(f'{i}.png','.png')
                app.frameCt += 1
                app.framet0 = time.time()

def loopTrail(app, temp, t0):
    while temp != []:
        if time.time() - t0 >= 0.1:
            temp[0].birth = time.time()
            app.trail.append(temp.pop(0))
            t0 = time.time()

def glowTrailMode_mouseDragged(app, event):
    # Create 2 particles upon drag
    # 20 particles max on screen to save your graphics card
    if (not app.record) and (app.top < event.y < app.bottom):
        if len(app.particles) < 20 and time.time() - app.t0 >= 0.01:
            vx, vy = random.randint(-15, 15) / 10, random.randint(-15, 15) / 10
            color = randomColor() if app.anyColor else app.pColor
            p = Particle(event.x, event.y, vx, vy, time.time(), color)
            pTrail = Particle(event.x, event.y, vx, vy, None, color)
            app.particles.append(p)
            app.temp.append(pTrail)
            app.t0 = time.time()

def glowTrailMode_mousePressed(app, event):
    x, y = event.x, event.y
    if app.record:
        if isClicked(app.next, x, y):
            f = app.getUserInput('How many frames do you want?')
            if f != None:
                app.maxFrames = int(f)
                app.path = askForPath(app)
                app.takeShots = True
                app.framet0 = time.time()
        if isClicked(app.back, x, y):
            app.record = False
            app.takeShots = False
            app.frameCt = 0
    else:
        if isClicked(app.back, x, y):
            app.mode = 'effectsMode'
            app.particles = []
            app.temp = []
            app.trail = []
            app.showTrail = None
            app.pColor = '#ffffff'
            app.anyColor = False
        elif isClicked(app.reset, x, y):
            app.temp = []
            app.trail = []
            app.showTrail = None
            app.pColor = '#ffffff'
            app.anyColor = False
        elif isClicked(app.eColor, x, y):
            app.anyColor = False
            color = askForColor(app)
            if color != None:
                app.pColor = color
            app.particles = []
            app.temp = []
        elif isClicked(app.randColor, x, y):
            app.anyColor = True
        elif isClicked(app.next, x, y):
            app.record = True

#################################################
# Smoke Mode
#################################################

def smokeMode_mousePressed(app, event):
    x, y = event.x, event.y
    if app.record:
        if isClicked(app.next, x, y):
            f = app.getUserInput('How many frames do you want?')
            if f != None:
                app.maxFrames = int(f)
                app.path = askForPath(app)
                app.takeShots = True
                app.framet0 = time.time()
        if isClicked(app.back, x, y):
            app.record = False
            app.takeShots = False
            app.frameCt = 0
    else:
        if isClicked(app.back, x, y):
            app.mode = 'effectsMode'
            app.pColor = '#ffffff'
            app.anyColor = False
            app.growSmoke = False
            app.smokeX, app.smokeY = None, None
            app.particles = []
        elif isClicked(app.eColor, x, y):
            app.anyColor = False
            color = askForColor(app)
            if color != None:
                app.pColor = color
        elif isClicked(app.randColor, x, y):
            app.anyColor = True
        elif isClicked(app.reset, x, y):
            app.pColor = '#ffffff'
            app.anyColor = False
            app.growSmoke = False
            app.smokeX, app.smokeY = None, None
            app.particles = []
        elif isClicked(app.next, x, y):
            app.record = True
        elif app.top < y < app.bottom:
            app.growSmoke = True
            app.smokeX, app.smokeY = x, y
        app.t0 = time.time()

def smokeMode_timerFired(app):
    if app.growSmoke and len(app.particles) < 40:
        if time.time() - app.t0 >= 0.01:
            cx, cy = app.smokeX, app.smokeY
            vx, vy = random.randint(-30, 30) / 10, random.randint(-80, -40) / 10
            color = randomColor() if app.anyColor else app.pColor
            p = Particle(cx, cy, vx, vy, time.time(), color)
            app.particles.append(p)
            app.t0 = time.time()
        emitParticles(app.particles, 1.5)
    if app.takeShots: # Save snapshots of the frame
        path = app.path
        if (path):
            i = app.frameCt
            if i < app.maxFrames and time.time() - app.framet0 >= 0.3:
                if (not path.endswith('.png')): path += '.png'
                path = path.replace('.png', f'{i}.png')
                result = ImageGrabber.grab((app.bbox))
                result.save(path)
                path = path.replace(f'{i}.png','.png')
                app.frameCt += 1
                app.framet0 = time.time()

#################################################
# Fireworks Mode
#################################################

def fireworksMode_mousePressed(app, event):
    x, y = event.x, event.y
    if app.record:
        if isClicked(app.next, x, y):
            f = app.getUserInput('How many frames do you want?')
            if f != None:
                app.maxFrames = int(f)
                app.path = askForPath(app)
                app.takeShots = True
                app.framet0 = time.time()
        if isClicked(app.back, x, y):
            app.record = False
            app.takeShots = False
            app.frameCt = 0
        elif app.top < y < app.bottom:
            growFireworks(app, x, y)
    else:
        if app.top < y < app.bottom:
            growFireworks(app, x, y)
        elif isClicked(app.back, x, y):
            app.mode = 'effectsMode'
            app.pColor = '#ffffff'
            app.anyColor = False
        elif isClicked(app.reset, x, y):
            app.pColor = '#ffffff'
            app.anyColor = False
        elif isClicked(app.eColor, x, y):
            app.anyColor = False
            color = askForColor(app)
            if color != None:
                app.pColor = color
        elif isClicked(app.randColor, x, y):
            app.anyColor = True
        elif isClicked(app.next, x, y):
            app.record = True

def growFireworks(app, x, y):
    app.growFireworks = True
    app.exploded = False
    if app.growFireworks:
        app.fireX, app.fireY = x, y
        app.v0 = - (- (2 * app.grav * (app.fireY - app.bottom))) ** 0.5
        color = randomColor() if app.anyColor else app.pColor
        app.seed = Particle(app.fireX, app.bottom, 0, app.v0, 
                            time.time(), color)
    else:
        app.fireX, app.fireY = None, None
        app.particles = []

def fireworksMode_timerFired(app):
    if app.growFireworks:
        if app.seed != None:
            t = time.time() - app.seed.birth
            app.seed.vy = app.v0 + app.grav * t
            app.seed.cy = app.bottom + app.v0*t + 0.5*app.grav*t**2
            if app.seed.vy >= 0:
                app.seed = None
                app.v0 = None
        else:
            if not app.exploded:
                explode(app)
            else:
                for particle in app.particles:
                    t = time.time() - particle.birth
                    particle.vy -= 5
                    particle.cy = app.fireY + particle.vy*t + 0.5*app.grav*t**2
                    particle.cx += particle.vx * t
                    dal = random.randint(10, 30) / 100
                    particle.alpha -= dal
                    if particle.alpha >= 0:
                        (r, g, b) = getAlphaColor(particle.color, 
                                    particle.alpha)
                        particle.color = rgbString(r, g, b)
                    if time.time() - particle.birth >= 0.4:
                        app.particles.remove(particle)
    if app.takeShots: # Save snapshots of the frame
        path = app.path
        if (path):
            i = app.frameCt
            if i < app.maxFrames and time.time() - app.framet0 >= 0.02:
                if (not path.endswith('.png')): path += '.png'
                path = path.replace('.png', f'{i}.png')
                result = ImageGrabber.grab((app.bbox))
                result.save(path)
                path = path.replace(f'{i}.png','.png')
                app.frameCt += 1
                app.framet0 = time.time()

def explode(app):
    for i in range(40):
        r = random.randint(50, 100)
        vx, vy = r*math.cos(math.pi*(i+1)/20), r*math.sin(math.pi*(i+1)/20)*4
        color = randomColor() if app.anyColor else app.pColor
        p = Particle(app.fireX, app.fireY, vx, vy, time.time(), color)
        app.particles.append(p)
    app.exploded = True

def fireworksMode_keyPressed(app, event):
    if event.key == 's': app.growFireworks = False

#################################################
# Saving: based on get&saveSnapshot() in 112 graphics
#################################################

def getBbox(app):
    # get the snapshot bounding box that only covers the camera frame
    app._showRootWindow()
    x0 = app._root.winfo_rootx() + app._canvas.winfo_x()
    y0 = app._root.winfo_rooty() + app._canvas.winfo_y() + 47 + app.top * 2
    x1 = x0 + app.width * 2
    y1 = y0 + app.width * 9 / 8
    return (x0, y0, x1, y1)

def askForPath(app):
    path = filedialog.asksaveasfilename(initialdir=os.getcwd(), 
           title='Select file: ',
           filetypes = (('png files','*.png'),('all files','*.*')))
    return path

#################################################
# Main App
#################################################

def appStarted(app):
    initCharacters(app)
    app.mode = 'welcomeMode'
    app.title = []
    app.transX, app.transY = 0, 0
    app.top = app.height/2-app.width*9/32
    app.bottom = app.height/2+app.width*9/32
    app.lines = []
    app.titleColor = 'white'
    app.uploaded = None
    app.timerDelay = 20
    welcomeScreen(app)

def isClicked(button, x, y):
    if button.name == '+' or button.name == '-':
        cx, cy = (button.x0 + button.x1) / 2, (button.y0 + button.y1) / 2
        r = cx - button.x0
        return distance(cx, cy, x, y) < r
    else:
        return (button.x0 < x < button.x1) and (button.y0 < y < button.y1)

def rgbString(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

def askForColor(app):
    r = app.getUserInput('Change color to (r value):')
    if r != None:
        g = app.getUserInput('Change color to (g value):')
        if g != None:
            b = app.getUserInput('Change color to (b value):')
            if b != None:
                r, g, b = int(r), int(g), int(b)
                if (0 <= r <= 255) and (0 <= g <= 255) and \
                    (0 <= b <= 255):
                    return rgbString(r, g, b)

# Reference:
# https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
def getRGBColor(h):
    h = h.lstrip('#')
    rgbColor = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    return rgbColor

# Reference:
# https://hangzone.com/calculate-implied-rgb-color-opacity-changes/
def getAlphaColor(color, alpha):
    alphaColor = tuple()
    r0, g0, b0 = getRGBColor(color)
    for channel in [r0, g0, b0]:
        new = int(alpha * channel + (1 - alpha) * 0)
        alphaColor += (new,)
    return alphaColor

def randomColor():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return rgbString(r, g, b)

#################################################
# redrawAll
#################################################

def drawBackground(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'black')

def welcomeMode_redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawTitle(app, canvas)
    canvas.create_text(app.width/2, app.height*0.82, fill = 'white',
                       text = 'PRESS ANYWHERE TO START', font = 'Helvetica 14')

def editMode_redrawAll(app, canvas):
    drawBackground(app, canvas)
    if app.uploaded:
        canvas.create_image(app.width/2, app.height/2,
                            image=ImageTk.PhotoImage(app.background))
    drawEditor(app, canvas)
    drawTitle(app, canvas)

def drawTitle(app, canvas):
    for charLines in app.lines:
        drawPlane(app, canvas, charLines[0])
        drawPlane(app, canvas, charLines[1])
        drawDepth(app, canvas, charLines)

def drawPlane(app, canvas, plane):
    for i in range(-1, len(plane)-1):
        x0, y0, x1, y1 = plane[i][0], plane[i][1], \
                         plane[i+1][0], plane[i+1][1]
        canvas.create_line(x0, y0, x1, y1, fill = app.titleColor)

def drawDepth(app, canvas, planes):
    planeA, planeB = planes[0], planes[1]
    for i in range(len(planeA)):
        x0, y0, x1, y1 = planeA[i][0], planeA[i][1], planeB[i][0], planeB[i][1]
        canvas.create_line(x0, y0, x1, y1, fill = app.titleColor)

def drawEditor(app, canvas):
    # show/hide menu button
    x0, y0 = app.toggleMenu.x0, app.toggleMenu.y0
    x1, y1 = app.toggleMenu.x1, app.toggleMenu.y1
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    canvas.create_rectangle(x0, y0, x1, y1, fill = app.toggleMenu.color)
    canvas.create_text(cx, cy, text = app.toggleMenu.name, font = 'Helvetica 15')
    # if the user clicks show menu, display all buttons on the menu
    if app.showMenu:
        drawRecButtons(app, canvas)
        drawCirButtons(app, canvas)
        canvas.create_text(app.width/2, app.height*0.82, 
                           text = 'PRESS ↑↓←→WS TO ROTATE CAMERA',
                           fill = 'white', font = 'Helvetica 14')
    drawFrame(app, canvas)
                       
def drawRecButtons(app, canvas):
    # all rectangular buttons on the menu
    for button in [app.editTitle, app.editColor, app.editBackground, app.reset, 
                   app.next, app.moveTitle]:
        canvas.create_rectangle(button.x0, button.y0, button.x1, button.y1,
                                fill = button.color)
        cx, cy = (button.x0 + button.x1) / 2, (button.y0 + button.y1) / 2
        canvas.create_text(cx, cy, text = button.name, font = 'Helvetica 15')

def drawCirButtons(app, canvas):
    # zoom in/out buttons
    for button in [app.zoomIn, app.zoomOut]:
        canvas.create_oval(button.x0, button.y0, button.x1, button.y1, 
                             fill = button.color, width = 0)
        cx, cy = (button.x0 + button.x1) / 2, (button.y0 + button.y1) / 2
        canvas.create_text(cx, cy, text = button.name, font = 'Helvetica 15')
    # max/min FOV warnings
    if app.maxFOV:
        cy = (app.zoomIn.y0 + app.zoomIn.y1) / 2
        canvas.create_text(app.zoomIn.x1 + 10, cy, text = 'MAXIMUM FOV REACHED',
                           fill = 'white', font = 'Helvetica 13', anchor = 'w')
    elif app.minFOV:
        cy = (app.zoomOut.y0 + app.zoomOut.y1) / 2
        canvas.create_text(app.zoomOut.x1 + 10, cy, text = 'MINIMUM FOV REACHED',
                           fill = 'white', font = 'Helvetica 13', anchor = 'w')

def backgroundMode_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'black')
    if app.uploaded:
        canvas.create_image(app.width/2, app.height/2,
                            image=ImageTk.PhotoImage(app.background))
        for button in [app.brighten, app.darken, app.blur, app.reset, 
                       app.contrastUp, app.contrastDown]:
            canvas.create_rectangle(button.x0, button.y0, button.x1, button.y1,
                                    fill = button.color, width = 0)
            cx, cy = (button.x0 + button.x1) / 2, (button.y0 + button.y1) / 2
            canvas.create_text(cx, cy, text = button.name, font = 'Helvetica 15')
        drawFrame(app, canvas)
        drawCornerButtons(app, canvas, ['BACK', 'OK'])
    else:
        for button in [app.upload, app.back]:
            canvas.create_rectangle(button.x0, button.y0, button.x1, button.y1,
                                    fill = button.color, width = 0)
            cx, cy = (button.x0 + button.x1) / 2, (button.y0 + button.y1) / 2
            if button.name == 'BACK':
                canvas.create_text(cx, cy, text = button.name, 
                                   font = 'Helvetica 15')
            else:
                canvas.create_text(cx, cy, text = button.name, 
                                   font = 'Helvetica 20')
        canvas.create_text(app.width/2, app.height*0.35, fill = 'white',
                       text = 'UPLOAD A 16:9 IMAGE FOR OPTIMAL PEFORMANCE',
                       font = 'Helvetica 20')

def drawCornerButtons(app, canvas, buttonNames):
    for i in range(2):
        button = [app.back, app.next][i]
        name = buttonNames[i]
        canvas.create_rectangle(button.x0, button.y0, button.x1, button.y1,
                                fill = button.color, width = 0)
        cx, cy = (button.x0 + button.x1) / 2, (button.y0 + button.y1) / 2
        canvas.create_text(cx, cy, text = buttonNames[i], font = 'Helvetica 15')

def moveTitleMode_redrawAll(app, canvas):
    drawBackground(app, canvas)
    if app.uploaded:
        canvas.create_image(app.width/2, app.height/2,
                            image=ImageTk.PhotoImage(app.background))
    canvas.create_text(app.width/2, app.height*0.82, 
                       text = 'DRAG OR PRESS ↑↓←→ TO MOVE TITLE',
                       fill = 'white', font = 'Helvetica 14')
    drawTitle(app, canvas)
    drawFrame(app, canvas)
    drawCornerButtons(app, canvas, ['RESET', 'OK'])

def drawFrame(app, canvas):
    canvas.create_line(0, app.height/2-app.width*9/32, app.width,
                       app.height/2-app.width*9/32, fill = 'red')
    canvas.create_line(0, app.height/2+app.width*9/32, app.width,
                       app.height/2+app.width*9/32, fill = 'red')

def effectsMode_redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawParticles(app.particles, canvas, 15)
    canvas.create_text(app.width/2, app.height*0.3,
                       text = 'CHOOSE YOUR EFFECT:', fill = 'white',
                       font = 'Helvetica 20')
    for button in [app.glowTrail, app.smoke, app.fireworks, app.back]:
        canvas.create_rectangle(button.x0, button.y0, button.x1, button.y1,
                                fill = button.color, width = 0)
        cx, cy = (button.x0 + button.x1) / 2, (button.y0 + button.y1) / 2
        if button.name == 'BACK':
            canvas.create_text(cx, cy, text = button.name, font = 'Helvetica 15')
        else:
            canvas.create_text(cx, cy, text = button.name, font = 'Helvetica 20')

def glowTrailMode_redrawAll(app, canvas):
    drawBackground(app, canvas)
    if app.uploaded:
        canvas.create_image(app.width/2, app.height/2,
                            image=ImageTk.PhotoImage(app.background))
    drawParticles(app.particles, canvas, 10)
    if app.particles == [] and app.showTrail:
        drawParticles(app.trail, canvas, 10)
    drawTitle(app, canvas)
    if app.record:
        drawSave(app, canvas)
    else:
        drawFrame(app, canvas)
        canvas.create_text(app.width/2, app.height*0.82, 
                        text = 'SLOWLY DRAG AND DROP MOUSE TO CREATE A GLOW TRAIL',
                        fill = 'white', font = 'Helvetica 14')
        canvas.create_text(app.width/2, app.height*0.85, 
                        text = 'RESET BEFORE ADJUSTING THE COLOR',
                        fill = 'white', font = 'Helvetica 14')
        for button in [app.back, app.next, app.eColor, app.reset, app.randColor]:
            canvas.create_rectangle(button.x0, button.y0, button.x1, button.y1,
                                    fill = button.color, width = 0)
            cx, cy = (button.x0 + button.x1) / 2, (button.y0 + button.y1) / 2
            canvas.create_text(cx, cy, text = button.name, font = 'Helvetica 15')   

def smokeMode_redrawAll(app, canvas):
    drawBackground(app, canvas)
    if app.uploaded:
        canvas.create_image(app.width/2, app.height/2,
                            image=ImageTk.PhotoImage(app.background))
    drawParticles(app.particles, canvas, 10)
    drawTitle(app, canvas)
    if app.record:
        drawSave(app, canvas)
    else:
        drawFrame(app, canvas)
        canvas.create_text(app.width/2, app.height*0.82,
                        text = 'CLICK INSIDE THE FRAME TO GROW SMOKE',
                        fill = 'white', font = 'Helvetica 14')
        for button in [app.back, app.next, app.eColor, app.randColor, app.reset]:
            canvas.create_rectangle(button.x0, button.y0, button.x1, button.y1,
                                    fill = button.color, width = 0)
            cx, cy = (button.x0 + button.x1) / 2, (button.y0 + button.y1) / 2
            canvas.create_text(cx, cy, text = button.name, font = 'Helvetica 15')

def fireworksMode_redrawAll(app, canvas):
    drawBackground(app, canvas)
    if app.uploaded:
        canvas.create_image(app.width/2, app.height/2,
                            image=ImageTk.PhotoImage(app.background))
    if app.seed != None:
        cx, cy, r = app.seed.cx, app.seed.cy, 5
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill = app.seed.color, 
                           width = 0)
    else:
        drawParticles(app.particles, canvas, 5)
    drawTitle(app, canvas)
    if app.record:
        drawSave(app, canvas)
    else:
        drawFrame(app, canvas)
        canvas.create_text(app.width/2, app.height*0.82,
                        text = 'CLICK INSIDE THE FRAME TO LAUNCH A FIREWORK',
                        fill = 'white', font = 'Helvetica 14')
        canvas.create_text(app.width/2, app.height*0.85, 
                        text = 'RESET BEFORE ADJUSTING THE COLOR',
                        fill = 'white', font = 'Helvetica 14')
        for button in [app.back, app.next, app.eColor, app.randColor, app.reset]:
            canvas.create_rectangle(button.x0, button.y0, button.x1, button.y1,
                                    fill = button.color, width = 0)
            cx, cy = (button.x0 + button.x1) / 2, (button.y0 + button.y1) / 2
            canvas.create_text(cx, cy, text = button.name, font = 'Helvetica 15')

def drawSave(app, canvas):
    canvas.create_text(app.width/2, app.height*0.82,
                       text = 'SAVE FRAMES AS A SEQUENCE OF IMAGES',
                       fill = 'white', font = 'Helvetica 14')
    drawCornerButtons(app, canvas, ['BACK', 'RECORD'])

def drawParticles(pList, canvas, r):
    for particle in pList:
        cx, cy = particle.cx, particle.cy
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill = particle.color, 
                           width = 0)

runApp(width=720, height=720)