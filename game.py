from visual import *
import visual as vs

print("""
BOUNCE GAME 2016
""")

global shootingBall
shootingBall = None

##GENERATE BALLS
def genBalls(count):
  balls = []
  for x in range(0, count):
    tempBall = sphere (color = (random.random(), random.random(), random.random()), pos=(random.random()+1, random.random()+1, random.random()+1), radius = 0.4, make_trail=False, retain=200);
    tempBall.p = vector (tempBall.pos.x, tempBall.pos.y, tempBall.pos.z)
    balls.append(tempBall);
  return balls

##SHOOTING
def hMousedown():  # handle mouse-DOWN event
    global shootingBall
    vss.unbind( 'mousedown', hMousedown) # STOP monitoring for mouse-down
    if shootingBall is None:
      shootingBall = sphere (color = color.red, radius = 0.1, make_trail=True, retain=200);
      shootingBall.p = -cam_frame.axis
    vss.bind( 'mousedown', hMousedown)  # START monitoring for mouse-down 

##CONFIG
win = vs.window(width = 1024, height = 720, menus=True, title='Bounce Game')
scene = vs.display( window=win, width=1024, height=720, forward=-vs.vector(1,1,2))
vss = scene
vss.userspin = False;
vss.userzoom = False;
vss.bind('mousedown',hMousedown)

cam_frame = vs.frame( pos = vs.vector(0,0,0,),  axis = (1,0,1))
fov = vs.pi/2.0
range_x = 4

xrotation = 0
yrotation = 0

cam_frame.axis.x = cos(yrotation)*sin(xrotation)
cam_frame.axis.z = cos(yrotation)*cos(xrotation)
cam_frame.axis.y = sin(yrotation)

vss.forward =  -cam_frame.axis 
vss.center =  cam_frame.pos
vss.fov = fov
vss.range = range_x

##SCENE
side = 10.0
thk = 0.3
s2 = 2*side - thk
s3 = 2*side + thk
wallR = box (pos=( side, 0, 0), size=(thk, s2, s3),  color = color.red)
wallL = box (pos=(-side, 0, 0), size=(thk, s2, s3),  color = color.red)
wallB = box (pos=(0, -side, 0), size=(s3, thk, s3),  color = color.blue)
wallT = box (pos=(0,  side, 0), size=(s3, thk, s3),  color = color.blue)
wallBK = box(pos=(0, 0, -side), size=(s2, s2, thk), color = (0.7,0.7,0.7))
wallBK2 = box(pos=(0, 0, side), size=(s2, s2, thk), color = (0.7,0.7,0.7))

##SCORE TEXT
totalScore = 0
scoreText = label(text = 'Score: %d'%totalScore, font='serif', pos=cam_frame.pos, border = 6,line=False, xoffset = 400, yoffset = -270)

##LIVES TEXT
livesLeft = 1
livesText = label(text = 'Lives: %d'%livesLeft, color=color.red, font='serif', pos=cam_frame.pos, border = 6,line=False, xoffset = 340, yoffset = -270)

##BALLS
ballCount = 5
killedBalls = 0
balls = genBalls(ballCount)

##BALLS TEXT
ballsText = label(text = 'Balls: %d'%ballCount, color=color.yellow, font='serif', pos=cam_frame.pos, border = 6,line=False, xoffset = -410, yoffset = -270)

##BOUNCE GAME CAPTION
text(text='Bounce Game', pos = (0,0,-9.7),
    align='center', depth=-0.3, material=materials.earth, height=2)

##MAIN GAME LOOP
ballRadius = 0.4
side = side - thk*0.5 - ballRadius

dt = 0.01
shootingDt = 0.4
t=0.0
while True:
  rate(100)

  ##KEYBOARD
  if scene.kb.keys:
    s = scene.kb.getkey()
    if(s == 'w' and (yrotation - vs.pi/30 >= -vs.pi/2)):
      yrotation -= vs.pi/30
    if(s == 's' and (yrotation + vs.pi/30 <= vs.pi/2)):
      yrotation += vs.pi/30
    if(s == 'a'):
      xrotation += vs.pi/30
    if(s == 'd'):
      xrotation -= vs.pi/30
    cam_frame.axis.x = cos(yrotation)*sin(xrotation)
    cam_frame.axis.z = cos(yrotation)*cos(xrotation)
    cam_frame.axis.y = sin(yrotation)

  vss.forward = -cam_frame.axis 

  ##BALL PHYSICS
  t = t + dt
  if shootingBall is not None:
    shootingBall.pos = shootingBall.pos + (shootingBall.p/1.0)*shootingDt
    if not (side > shootingBall.x > -side) or not (side > shootingBall.y > -side) or not (side > shootingBall.z > -side):
      shootingBall.visible = False
      shootingBall.trail_object.visible = False
      del shootingBall
      shootingBall = None
  for ba in balls:
    ba.pos = ba.pos + (ba.p/1.0)*dt
    ballRemoved = False
    if shootingBall is not None:
      calculatedCollsionFormula = (ba.pos.x - shootingBall.pos.x)**2+(ba.pos.y - shootingBall.pos.y)**2+(ba.pos.z - shootingBall.pos.z)**2
      calulatedRadius = (ba.radius+shootingBall.radius)**2
      if (calculatedCollsionFormula <= calulatedRadius):
        shootingBall.visible = False
        shootingBall.trail_object.visible = False
        del shootingBall
        shootingBall = None
        ba.visible = False
        balls.remove(ba)
        ballRemoved = True
        del ba
        killedBalls += 1
        totalScore += 1
        scoreText.text = 'Score: %d'%totalScore
        ballsText.text = 'Balls: %d'%(ballCount-killedBalls)
    if not ballRemoved:
      if not (side > ba.x > -side):
        ba.p.x = -ba.p.x
      if not (side > ba.y > -side):
        ba.p.y = -ba.p.y
      if not (side > ba.z > -side):
        ba.p.z = -ba.p.z
      calculatedCollsionFormula = (ba.pos.x)**2+(ba.pos.y)**2+(ba.pos.z)**2
      calulatedRadius = (ba.radius+0.4)**2
      if(calculatedCollsionFormula <= calulatedRadius):
        livesLeft -= 1
        livesText.text = 'Lives: %d'%livesLeft
        if(livesLeft==0):
          dt = 0
          vss.userspin = True;
          vss.userzoom = True;
          vss.unbind( 'mousedown', hMousedown)
          ba.color = color.red
          del balls[:]
          sphere (color = color.green, pos=(0,0,0), radius = 0.4, make_trail=False, retain=200);
        else:
          ba.visible = False
          balls.remove(ba)
          del ba
          killedBalls += 1

  ##GAME SCORE
  if(killedBalls >= ballCount):
    ballCount += 3
    killedBalls = 0
    balls = genBalls(ballCount)
    ballsText.text = 'Balls: %d'%ballCount
    dt += 0.01
        

