// STLio
// by Bereket Abraham using the unlekker library by Marius Watz
// unlekker.geom.PolyData.

import unlekker.data.*;
import unlekker.geom.*;

STL stl;
FaceList poly;
PrintWriter output;
//ArrayList datalist;
//String filename,data[];

void setup() {
  size(500,350, P3D);
  frameRate(25);
  sphereDetail(12);
  //datalist=new ArrayList();
  
  readSTL();
  String filename = "faces.txt";
  output = createWriter(filename); 
  
  if(poly!=null) {
    int len = poly.num;
    Face[] faces = poly.f;
    for(int i=0; i<len; i++) {
      //datalist.add(""+val);
      Face face = faces[i];
      
      for(int j=0; j<face.v.length; j++) {
        output.print(face.v[j]);
    	output.print(",");
      }
      output.println("");
    }
  }
  
  output.flush();
  output.close();
  //data=new String[datalist.size()];
  //data=(String [])datalist.toArray(data);  
  //saveStrings(filename, data);
  println("Saved data to '"+filename+".");
  
}

void draw() {
  translate(width/2,height/2);

  // If data has been read, then draw it
  if(poly!=null) {
    background(0);
    noStroke();
    lights();
    rotateY(radians(frameCount));
    rotateX(radians(frameCount*0.25f));
    fill(0,200,255, 128);

    poly.draw(this);
  }
}

void readSTL() {
  // Read STL file
  stl=new STL(this,"test3.stl");

  // Get polygon data
  poly=stl.getPolyData();

  poly.normalize(100); // normalize object to 400 radius
  poly.center(); // center it around world origin
}

void outputSTL() {
  float rad;

  // Initialize STL output
  stl=(STL)beginRaw("unlekker.data.STL","test3.stl");

  // Draw random shapes
  for(int i=0; i<200; i++) {
    pushMatrix();
    translate(random(-200,200),0,-random(400));
    rotateX(((float)(int)random(6))*radians(30));
    rotateY(((float)(int)random(6))*radians(30));

    rad=random(5,25);
    if(random(100)>5) box(rad,random(50,200),rad);
    else sphere(rad);
    popMatrix();
  }
  
  // End STL output
  endRaw();
}

void keyPressed() {
  exit();
}