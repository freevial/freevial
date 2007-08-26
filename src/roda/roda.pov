union {
   //*PMName RodaTextos
   
   text {
      //*PMName cat1
      ttf "/home/carles/.fonts/Eurostile Extended Black.ttf"
      "          Personatges i events"
      1, <0, 0>
      scale <0.3, 0.4, 0.3>
      rotate x*90
      
      pigment {
         color rgbf <0.07451, 0.16863, 1, 0.2>
      }
      
      finish {
         diffuse 0.5
         brilliance 0.5
         
         reflection {
            rgb <1, 1, 1>, rgb <0, 0, 0>
         }
      }
   }
   
   text {
      //*PMName cat2
      ttf "/home/carles/.fonts/Eurostile Extended Black.ttf"
      "          Ubuntu"
      1, <0, 0>
      scale <0.3, 0.4, 0.3>
      rotate <90, -60, 0>
      
      pigment {
         color rgbf <1, 0.50196, 0, 0.2>
      }
      
      finish {
         diffuse 0.5
         brilliance 0.5
         
         reflection {
            rgb <1, 1, 1>, rgb <0, 0, 0>
         }
      }
   }
   
   text {
      //*PMName cat3
      ttf "/home/carles/.fonts/Eurostile Extended Black.ttf"
      "          Internet"
      1, <0, 0>
      scale <0.3, 0.4, 0.3>
      rotate <90, -120, 0>
      
      pigment {
         color rgbf <0, 1, 0, 0.2>
      }
      
      finish {
         diffuse 0.5
         brilliance 0.5
         
         reflection {
            rgb <1, 1, 1>, rgb <0, 0, 0>
         }
      }
   }
   
   text {
      //*PMName cat4
      ttf "/home/carles/.fonts/Eurostile Extended Black.ttf"
      "          Jocs i pelis"
      1, <0, 0>
      scale <0.3, 0.4, 0.3>
      rotate <90, -180, 0>
      
      pigment {
         color rgbf <1, 0, 0, 0.2>
      }
      
      finish {
         diffuse 0.5
         brilliance 0.5
         
         reflection {
            rgb <1, 1, 1>, rgb <0, 0, 0>
         }
      }
   }
   
   text {
      //*PMName cat5
      ttf "/home/carles/.fonts/Eurostile Extended Black.ttf"
      "          Terminal i llenguatges"
      1, <0, 0>
      scale <0.3, 0.4, 0.3>
      rotate <90, -240, 0>
      
      pigment {
         color rgbf <1, 0, 1, 0.2>
      }
      
      finish {
         diffuse 0.5
         brilliance 0.5
         
         reflection {
            rgb <1, 1, 1>, rgb <0, 0, 0>
         }
      }
   }
   
   text {
      //*PMName cat6
      ttf "/home/carles/.fonts/Eurostile Extended Black.ttf"
      "          Programari i maquinari"
      1, <0, 0>
      scale <0.3, 0.4, 0.3>
      rotate <90, -300, 0>
      
      pigment {
         color rgbf <1, 1, 0, 0.2>
      }
      
      finish {
         diffuse 0.5
         brilliance 0.5
         
         reflection {
            rgb <1, 1, 1>, rgb <0, 0, 0>
         }
      }
   }
   translate y*0.5
   rotate y*(frame_number*10)
}

difference {
   //*PMName cubilet
   
   cylinder {
      <0, 0, 0>, <0, -1.5, 0>, 6
      scale 1
      rotate <0, 0, 0>
      translate <0, 0, 0>
   }
   
   pigment {
      color rgb <0.83922, 0.83922, 0.83922>
   }
   
   finish {
      brilliance 1
      specular 0.5
      
      reflection {
         rgb <0.580392, 0.580392, 0.580392>, rgb <0, 0, 0>
      }
   }
}

global_settings {
   adc_bailout 0.0039216
   assumed_gamma 1.5
   noise_generator 2
}

light_source {
   <4, 5, -5>, rgb <1, 1, 1>
}

camera {
   perspective
   location <3, 7, -0.5>
   sky <0, 1, 0>
   direction <0, 0, 1>
   right <1, 0, 0>
   up <0, 1, 0>
   look_at <3, 0, -0.22597>
}
