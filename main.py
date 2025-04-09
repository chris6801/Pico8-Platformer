--loop

function _init()
      make_player()
end

function _update()
 p:get_input()
      update_objs()
end

function _draw()
 cls()
 map()
      draw_objs()
      print("y")
      print(p.y)
      print("dy")
      print(p.dy)
      print("ax")
      print(p.ax)
      print("on ground")
      print(p.on_ground)
end

--physics and utils
gravity=.1
friction=.85
tile_size=8

objs={}

function update_objs()
      for obj in all(objs) do
            obj:update()
      end
end

function draw_objs()
      for obj in all(objs) do
            animate(obj)
            obj:draw()
      end
end

function
detect_collisions(subject,objs)
      new_x=subject.x+subject.dx
      new_y=subject.y+subject.dy
      for obj in all(objs) do
            if obj.x < subject.x
            < obj.x+tile_size then
                  if subject.dx > 0 then
                        subject.x=obj.x
                  elseif subject.dx < 0 then
                   subject.x=obj.x+tile_size
                  end
            end
            if subject.dy>0 then
                  if obj.y<subject.y+
                  tile_size<obj.y+tile_size then
                        subject.dy=obj.y-subject.y
                  end
            elseif subject.dy<0 then
                  if obj.y<subject.y<obj.y+
                  tile_size then
                   subjet.dy=obj.y-subject.y
                  end
            end
      end
end

--tile approach
dirs={{0,1},{1,-1},{0,-1},{-1,-1},
{-1,0},{-1,1},{0,1},{1,1}}

function tile2screen(x,y)
      return x*8,y*8
end

function screen2tile(x,y)
      return flr(x/8),flr(y/8)
end

function check_col(subj)
      local x,y=subj.x,subj.y
      if subj.dx>0 then
            local tx,ty=screen2tile(x+subj.w,y)
            local new_x,new_y=x+subj.dx+subj.w,
            y+subj.dy
       local new_tx,new_ty=screen2tile(
            new_x,new_y)
            --check x first
            local tile=mget(new_tx,ty)
            local solid=fget(tile,0)
            --add dx check here
            if solid then
                  subj.dx=0
            end
      
      end
      --then y
      if subj.dy>0 then
            --x,y=x,y+subj.h
            tx,ty=screen2tile(x,y+subj.h)
            new_x,new_y=x+subj.dx,y+subj.dy+subj.h
            new_tx,new_ty=screen2tile(new_x,
            new_y)
            tile=mget(tx,new_ty)
            solid=fget(tile,0)
            if solid then
                        subj.dy=0
                        subj.on_ground=true
            end
      elseif subj.dy<0 then
            --x,y=x,y+subj.h
            tx,ty=screen2tile(x,y)
            new_x,new_y=x+subj.dx,y+subj.dy
            new_tx,new_ty=screen2tile(new_x,
            new_y)
            tile=mget(tx,new_ty)
            solid=fget(tile,0)
            if solid then
                        subj.dy=0
            end
      end
end

--animation
function animate(x)
      if x.play~=x.state then
            x.play=x.state
            x.a_idx=1
            x.anim_t=0
            print(x.play)
      elseif #x.anims[x.play]>1 then
       x.anim_t+=1
       if x.anim_t %
       (x.anims[x.play].fr)==0 then
            x.a_idx=(x.a_idx %
            #x.anims[x.play])+1
            if x.a_idx==1 and
            x.anims[x.play].next then
                  x.state=x.anims[x.play].next
                  x.play=x.state
                  end
  end
      end
      x.spr=x.anims[x.state][x.a_idx]
end

--player
jump_power=-2

function make_player()
      p={
            x=64,
            y=64,
            w=8,
            h=8,
            dx=0,
            dy=0,
            ax=0,
            ay=0,
            on_ground=true,
            a_idx=1,
            anim_t=1,   
            play="idle",      
            state="idle",
            anims={
                  idle={fr=15,1,2},
                  walk={fr=10,3,4},
            },
            spr=1,
            get_input=function(self)
                  if btn(⬅️) then
                        self.ax=-1
                  elseif btn(➡️) then
                        self.ax=1
                  else
                        self.ax=0
                  end
                  if btnp(❎) and
                   self.on_ground then
                        self.dy=jump_power
                        self.on_ground=false
                  end
            end,
            update=function(self)
             self.dx*=friction
             self.ay=gravity
            
             self.dx+=self.ax
             self.dy+=self.ay
            
             self.dy=min(self.dy,6)
             check_col(self)
            
             --check state
             if abs(self.dx)>0 then
                  self.state="walk"
             else
                  self.state="idle"
   end
            
                  self.x+=self.dx
                  self.y+=self.dy
            end,
            draw=function(self)
             spr(self.spr,self.x,self.y)
            end,
      }
      add(objs,p)             
end
