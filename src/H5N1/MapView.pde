
import Frame;

public class MapView extends Frame {
    
    
    MapView
 
 public void draw() {
  
   // Use open gl to do the coordinate translation.
  pushMatrix();
  translate(x, y);
  
  // --------------- Your Drow funtions Here
  
  triangle(15, 0, 0, 15, 30, 15);
  rect(0, 15, 30, 30);
  rect(12, 30, 10, 15);
  
  // -----------------------------------
  
  popMatrix();
 } 
 
}
