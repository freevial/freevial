
/***********************************************************/
/*                                                         */
/* Applet pel disseny de les figures pel Freevial          */
/*                                                         */
/* Carles 21/08/2007                                       */
/*                                                         */
/* Estructura disenyada en kpovmodeler i adaptada          */
/* per afegir modificacions programàtiques                 */
/*                                                         */
/***********************************************************/


#declare punt_transparent = 1;
#declare punt_opac = 0;

#declare punt_intens = 0.6;

/**************************************************/

#declare punt_groc = punt_opac;
#declare punt_rosa = punt_opac;
#declare punt_blau = punt_opac;
#declare punt_taronja = punt_opac;
#declare punt_vermell = punt_opac;
#declare punt_verd = punt_opac;

/***************************************************/

#declare efectepeces = finish {
   diffuse 0.5
   brilliance 0.5
   
   reflection {
      rgb <1, 1, 1>, rgb <0, 0, 0>
   }
}

difference {
   //*PMName cubilet
   
   cylinder {
      <0, 0, 0>, <0, -1.5, 0>, 6
      scale 1
      rotate <0, 0, 0>
      translate <0, 0, 0>
   }
   
   union {
      //*PMName logo_ubuntu
      
      union {
         //*PMName f1
         
         difference {
            //*PMName arc1
            
            cylinder {
               <0, 0.5, 0>, <0, -0.5, 0>, 4.1
               scale 1
               rotate <0, 0, 0>
               translate <0, 0, 0>
            }
            
            cylinder {
               <0, 0.6, 0>, <0, -0.6, 0>, 2.4
               scale 1
               rotate <0, 0, 0>
               translate <0, 0, 0>
            }
            
            cylinder {
               <0, 0.7, 0>, <0, -0.7, 0>, 1.5
               scale 1
               rotate <0, 0, 0>
               translate <-2.87986, 0, -3.5872>
            }
            
            box {
               <-4.1, -0.7, 0>, <4.1, 0.7, 5>
               scale 1
               rotate <0, 0, 0>
               translate <0, 0, 0>
            }
            
            box {
               <0, -0.7, 0>, <4.1, 0.7, -5>
               scale 1
               rotate y*(-18)
               translate <0, 0, 0>
            }
         }
         
         cylinder {
            //*PMName punt1
            <0, 0.5, 0>, <0, -0.5, 0>, 1.1
            scale 1
            rotate <0, 0, 0>
            translate <-2.87986, 2.30782e-15, -3.5872>
         }
      }
      
      union {
         //*PMName f2
         
         difference {
            //*PMName arc1
            
            cylinder {
               <0, 0.5, 0>, <0, -0.5, 0>, 4.1
               scale 1
               rotate <0, 0, 0>
               translate <0, 0, 0>
            }
            
            cylinder {
               <0, 0.6, 0>, <0, -0.6, 0>, 2.4
               scale 1
               rotate <0, 0, 0>
               translate <0, 0, 0>
            }
            
            cylinder {
               <0, 0.7, 0>, <0, -0.7, 0>, 1.5
               scale 1
               rotate <0, 0, 0>
               translate <-2.87986, 0, -3.5872>
            }
            
            box {
               <-4.1, -0.7, 0>, <4.1, 0.7, 5>
               scale 1
               rotate <0, 0, 0>
               translate <0, 0, 0>
            }
            
            box {
               <0, -0.7, 0>, <4.1, 0.7, -5>
               scale 1
               rotate y*(-18)
               translate <0, 0, 0>
            }
         }
         
         cylinder {
            //*PMName punt1
            <0, 0.5, 0>, <0, -0.5, 0>, 1.1
            scale 1
            rotate <0, 0, 0>
            translate <-2.87986, 2.30782e-15, -3.5872>
         }
         rotate y*120
      }
      
      union {
         //*PMName f3
         
         difference {
            //*PMName arc1
            
            cylinder {
               <0, 0.5, 0>, <0, -0.5, 0>, 4.1
               scale 1
               rotate <0, 0, 0>
               translate <0, 0, 0>
            }
            
            cylinder {
               <0, 0.6, 0>, <0, -0.6, 0>, 2.4
               scale 1
               rotate <0, 0, 0>
               translate <0, 0, 0>
            }
            
            cylinder {
               <0, 0.7, 0>, <0, -0.7, 0>, 1.5
               scale 1
               rotate <0, 0, 0>
               translate <-2.87986, 0, -3.5872>
            }
            
            box {
               <-4.1, -0.7, 0>, <4.1, 0.7, 5>
               scale 1
               rotate <0, 0, 0>
               translate <0, 0, 0>
            }
            
            box {
               <0, -0.7, 0>, <4.1, 0.7, -5>
               scale 1
               rotate y*(-18)
               translate <0, 0, 0>
            }
         }
         
         cylinder {
            //*PMName punt1
            <0, 0.5, 0>, <0, -0.5, 0>, 1.1
            scale 1
            rotate <0, 0, 0>
            translate <-2.87986, 2.30782e-15, -3.5872>
         }
         rotate y*(-120)
      }
      scale 1
      translate y*(-0.1)
   }
   
   pigment {
      color rgbt <0.027451, 0.0627451, 0.364706 >
   }
   
   finish {
      specular 0.5
      
      reflection {
         rgb <0.580392, 0.580392, 0.580392>, rgb <0, 0, 0>
      }
   }
}

union {
   //*PMName logo_ubuntu
   


   union {
      //*PMName f1
      
		#if ( punt_rosa = punt_opac )
      difference {
         //*PMName arc1
         
         cylinder {
            <0, 0.5, 0>, <0, -0.5, 0>, 4
            scale 1
            rotate <0, 0, 0>
            translate <0, 0, 0>
         }
         
         cylinder {
            <0, 0.6, 0>, <0, -0.6, 0>, 2.5
            scale 1
            rotate <0, 0, 0>
            translate <0, 0, 0>
         }
         
         cylinder {
            <0, 0.7, 0>, <0, -0.7, 0>, 1.5
            scale 1
            rotate <0, 0, 0>
            translate <-2.87986, 0, -3.5872>
         }
         
         box {
            <-4.1, -0.7, 0>, <4.1, 0.7, 5>
            scale 1
            rotate <0, 0, 0>
            translate <0, 0, 0>
         }
         
         box {
            <0, -0.7, 0>, <4.1, 0.7, -5>
            scale 1
            rotate y*(-18)
            translate <0, 0, 0>
         }
         
         pigment {
            color rgbft <1, 0, 1, punt_intens, punt_rosa>
         }
         
         finish {
            efectepeces
         }
      }
	#end
    
		#if ( punt_groc = punt_opac )
      cylinder {
         //*PMName punt1
         <0, 0.5, 0>, <0, -0.5, 0>, 1
         
         pigment {
            color rgbft <1, 1, 0, punt_intens, punt_groc>
         }
         
         finish {
            efectepeces
            diffuse 0.6
            brilliance 1
            metallic 100
            
            reflection {
               rgb <1, 1, 1>, rgb <0, 0, 0>
            }
         }
         scale 1
         rotate <0, 0, 0>
         translate <-2.87986, 2.30782e-15, -3.5872>
      }
	  #end
   }
   

   union {
      //*PMName f2

#if ( punt_taronja = punt_opac )
      difference {
         //*PMName arc1
         
         cylinder {
            <0, 0.5, 0>, <0, -0.5, 0>, 4
         }
         
         cylinder {
            <0, 0.6, 0>, <0, -0.6, 0>, 2.5
         }
         
         cylinder {
            <0, 0.7, 0>, <0, -0.7, 0>, 1.5
            translate <-2.87986, 0, -3.5872>
         }
         
         box {
            <-4.1, -0.7, 0>, <4.1, 0.7, 5>
         }
         
         box {
            <0, -0.7, 0>, <4.1, 0.7, -5>
            rotate y*(-18)
         }
         
         pigment {
            color rgbft <1, .6, 0, punt_intens, punt_taronja>
         }
         
         finish {
            efectepeces
         }
      }
#end

    
		#if ( punt_blau = punt_opac )
      cylinder {
         //*PMName punt1
         <0, 0.5, 0>, <0, -0.5, 0>, 1
         
         pigment {
            color rgbft <0, 1, 1, punt_intens, punt_blau>
         }
         
         finish {
            efectepeces
         }
         translate <-2.8799, 0, -3.5872>
      }
#end


      rotate y*120
   }
   

   union {
      //*PMName f3
      
		#if ( punt_verd = punt_opac )
      difference {
         //*PMName arc1
         
         cylinder {
            <0, 0.5, 0>, <0, -0.5, 0>, 4
         }
         
         cylinder {
            <0, 0.6, 0>, <0, -0.6, 0>, 2.5
         }
         
         cylinder {
            <0, 0.7, 0>, <0, -0.7, 0>, 1.5
            translate <-2.87986, 0, -3.5872>
         }
         
         box {
            <-4.1, -0.7, 0>, <4.1, 0.7, 5>
         }
         
         box {
            <0, -0.7, 0>, <4.1, 0.7, -5>
            rotate y*(-18)
         }
         
         pigment {
            color rgbft <0, 1, 0, punt_intens, punt_verd>
         }
         
         finish {
            efectepeces
         }
      }
#end
      
		#if ( punt_vermell = punt_opac )
      cylinder {
         //*PMName punt1
         <0, 0.5, 0>, <0, -0.5, 0>, 1
         
         pigment {
            color rgbft <1, 0, 0, punt_intens, punt_vermell>
         }
         
         finish {
            efectepeces
         }
         translate <-2.8799, 0, -3.5872>
      }
	#end


      rotate y*(-120)
   }
   translate <0, 0, 0>
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
   location <8.5, 13, 1>
   sky <0, 1, 0>
   direction <0, 0, 1>
   right <1, 0, 0>
   up <0, 1, 0>
   look_at <0,0,0>
}
