/*
  <x0, y0>
  (0,0) ----------------------------> x+
  |
  |
  |
  |
  |                      <x1, y1>
  y+
*/

public class RECT {    
  public int x0, y0, // left, top
  public int x0, y1; // right, bottom
  
  public RECT( x0ft, y0, x1, y1 ){
    this.x0 = x0;  // left
    this.y0 = y0;  // top
    this.x1 = x1;  // right
    this.y1 = y1;  // bottom   
  } 
  
  bool IsInSide(int x, int y, int r)
  {
    if( x0 -r <=  x <= x1 + r
        && y0 -r <= y <= y1 + r) 
        return true;

    return false;
  }
}


public class Frame {
  
  public RECT worldDimension; // Dimension with respect to world coordinates.
  public RECT dimension;      // Dimension with respect to local coordinates.
  
  public Frame(RECT worldDimension)
  {
    // TODO: store world and convet to local.
  }
  
 
  public void StartDraw() {
    pushMatrix();
    translate(worldDimension.x0, worldDimension.y0);
  }
  
  
  public void EndDraw() {
  popMatrix();
 } 
 
}
