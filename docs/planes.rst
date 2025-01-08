.. _planesreq:

Planes Required Reading
=======================

                                                                
Abstract                                                  
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                                  
 | CSPICE contains a substantial set of subroutines that solve common  
   mathematical problems involving planes.                             
                                                               
Introduction                                              
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                                  
 | In CSPICE, the \`plane' is a data representation describing planes  
   in three-dimensional space. The purpose of the plane data type is   
   to simplify the calling sequences of some geometry routines. Also,  
   using a "plane" data type helps to centralize error checking and    
   facilitate conversion between different representations of planes.  
                                                               
References                                                
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                                            
                                                                       
#. \`Calculus, Vol. II'. Tom Apostol. John Wiley and Sons,      
   * See Chapter 5, \`Eigenvalues of Operators Acting on Euclidean Spaces'.                                                            
                                                                       
#. Ellipses required reading                                    
   (`ellipses.req <../req/ellipses.html>`__).                          
                                                                       
                                                
                                                                       
Plane Data Type Description                               
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                                  
 | NAIF defines a SPICE plane using a unit vector N, normal to the     
   plane, and a scalar constant C. Let                                 
                                                                       
 ::                                                                    
                                                                       
       < X, Y >                                                        
                                                                       
 denote the inner product of the vectors X and Y, then the             
 relationship                                                          
 ::                                                                    
                                                                       
       < X, N > = C                                                    
                                                                       
 holds for all vectors X in the plane. C is the distance of the plane  
 from the origin. The vector                                           
 ::                                                                    
                                                                       
       C * N                                                           
                                                                       
 is the closest point in the plane to the origin. For planes that do   
 not contain the origin, the vector N points from the origin toward    
 the plane.                                                            
 The internal design of the plane data type is not part of its         
 specification. The design is an implementation choice based on the    
 programming language and so the design may change. Users should not   
 write code based on the current implementation; such code might fail  
 when used with a future version of CSPICE.                            
                                                                       
 NAIF implemented the SPICE plane data type in C as a structure with   
 the fields                                                            
                                                                       
 ::                                                                    
                                                                       
          SpiceDouble      normal   [3];                               
          SpiceDouble      constant;                                   
                                                                       
 'normal' contains the unit normal vector N; 'constant' contains the   
 plane constant C.                                                     
                                
                                                                       
Plane routines                                            
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                             
                                
                                                                       
Constructing planes                                       
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                                            
 | The CSPICE routines that create SPICE planes from various forms of  
   data that define geometric planes:                                  
                                                                       
 `nvc2pl_c <../cspice/nvc2pl_c.html>`__                                
    Normal vector and constant to plane                                
                                                                       
 `nvp2pl_c <../cspice/nvp2pl_c.html>`__                                
    Normal vector and point to plane                                   
                                                                       
 `psv2pl_c <../cspice/psv2pl_c.html>`__                                
    Point and spanning vectors to plane                                
                                                                       
 CSPICE routines that take planes as input arguments can accept planes 
 created by any of the routines listed above.                          
 The information stored in SPICE planes is not necessarily the input   
 information you supply to a plane-making routine. SPICE planes use a  
 single, uniform internal representation for planes, no matter what    
 data you use to create them. As a consequence, when you create a      
 SPICE plane and then break it apart into data that define a plane,    
 the returned data will not necessarily be the data you originally     
 supplied, though they define the same geometric plane as the data you 
 originally supplied.                                                  
                                                                       
 This \`loss of information' may seem to be a liability at first but   
 turns out to be a convenience in the end: the CSPICE routines that    
 break apart SPICE planes into various representations return outputs  
 that are particularly useful for many geometric computations. In the  
 case of the routine `pl2nvp_c <../cspice/pl2nvp_c.html>`__ (Plane to  
 normal vector and point), the output normal vector is always a unit   
 vector, and the output point is always the closest point in the plane 
 to the origin. The normal vector points from the origin toward the    
 plane, if the plane does not contain the origin.                      
                                                                       
 You can convert any of the following representations of planes to a   
 SPICE plane:                                                          
                                                                       
 **A normal vector and a constant**                                                      
    If N is a normal vector and C is a constant, then the plane is the 
    set of points X such that                                          
                                                                       
 ::                                                                    
                                                                       
                                  < X, N > = C.                        
                                                                       
 **A normal vector and a point**                                                         
    If P is a point in the plane and N is a normal vector, then the    
    plane is the set of points X such that                             
                                                                       
 ::                                                                    
                                                                       
                                  < X - P,  N > = 0.                   
                                                                       
 **A point and two spanning vectors**                                                    
    If P is a point in the plane and V1 and V2 are two linearly        
    independent but not necessarily orthogonal vectors, then the plane 
    is the set of points                                               
                                                                       
 ::                                                                    
                                                                       
                                  P   +   s * V1   +   t * V2,         
                                                                       
    where s and t are real numbers.                                    
                                                                       
 The calling sequences of the CSPICE routines that create planes are   
 described below. For examples of how you might use these routines in  
 a program, see the Examples section.                                  
                                
                                                                       
Construct a plane from a normal vector and constant       
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                                            
 | Let \`n' represent a vector normal to a plane, and \`c', a scalar   
   constant.                                                           
                                                                       
 Let \`n', \`c' and \`plane' be declared by                            
                                                                       
 ::                                                                    
                                                                       
       SpiceDouble          n[3];                                      
       SpiceDouble          c;                                         
       SpicePlane           plane;                                     
                                                                       
 After \`n' and \`c' have been assigned values, you can construct a    
 SPICE plane that represents the plane having normal \`n' and constant 
 \`c' by calling `nvc2pl_c <../cspice/nvc2pl_c.html>`__:               
 ::                                                                    
                                                                       
       nvc2pl ( n, c, &plane );                                      
                                                                       
                                                
                                                                       
Construct a plane from a normal vector and a point        
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                                            
 | Let \`n' represent a vector normal to a plane, and \`p', a point on 
   the plane.                                                          
                                                                       
 Declare \`n', \`p', and \`plane' as:                                  
                                                                       
 ::                                                                    
                                                                       
       SpiceDouble          n[3];                                      
       SpiceDouble          p[3];                                      
       SpicePlane           plane;                                     
                                                                       
 After \`n' and \`p' have been assigned values, you can construct a    
 SPICE plane that represents the plane containing point \`p' and       
 having normal \`n' by calling `nvp2pl_c <../cspice/nvp2pl_c.html>`__: 
 ::                                                                    
                                                                       
       nvp2pl ( n, p,  &plane );                                     
                                                                       
                                                
                                                                       
Construct a plane from a point and spanning vectors       
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                                            
 | Let \`p' represent a point on a plane, \`v1' and \`v2', two vectors 
   in the plane.                                                       
                                                                       
 Let \`p', \`v1', \`v2', and \`plane' be declared by                   
                                                                       
 ::                                                                    
                                                                       
       ConstSpiceDouble    point[3];                                   
       ConstSpiceDouble    span1[3];                                   
       ConstSpiceDouble    span2[3];                                   
       SpicePlane          plane;                                      
                                                                       
 After \`p', \`v1', and \`v2' have been assigned values, you can       
 construct a SPICE plane that represents the plane spanned by the      
 vectors V1 and V2 and containing the point P by calling               
 `psv2pl_c <../cspice/psv2pl_c.html>`__:                               
 ::                                                                    
                                                                       
       psv2pl ( p, v1, v2, &plane );                                 
                                                                       
                                                
                                                                       
Access plane data elements                                
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                                            
 | You can \`take planes apart' as well as put them together. Any      
   SPICE plane, regardless of which routine created it, can be         
   converted to any of the representations listed in the previous      
   section: normal vector and constant, point and normal vector, or    
   point and spanning vectors.                                         
                                                                       
 The CSPICE routines that break planes apart into data that define     
 geometric planes are                                                  
                                                                       
 `pl2nvc_c <../cspice/pl2nvc_c.html>`__                                
    Plane to normal vector and constant                                
                                                                       
 `pl2nvp_c <../cspice/pl2nvp_c.html>`__                                
    Plane to normal vector and point                                   
                                                                       
 `pl2psv_c <../cspice/pl2psv_c.html>`__                                
    Plane to point and spanning vectors                                
                                                                       
 In the following discussion, \`plane' is a SPICE plane, \`n' is a     
 normal vector, \`p' is a point, \`c' is a scalar constant, and V1 and 
 V2 are spanning vectors. We omit the declarations; all are as in the  
 previous section.                                                     
 To find a unit normal vector \`n' and a plane constant \`c' that      
 define \`plane', use `pl2nvc_c <../cspice/pl2nvc_c.html>`__:          
                                                                       
 ::                                                                    
                                                                       
       pl2nvc ( &plane, n, &c );                                     
                                                                       
 The constant \`c' is the distance of the plane from the origin. The   
 vector                                                                
 ::                                                                    
                                                                       
       C * N                                                           
                                                                       
 will be the closest point in the plane to the origin.                 
 To find a unit normal vector \`n' and a point \`p' that define        
 \`plane', use `pl2nvp_c <../cspice/pl2nvp_c.html>`__:                 
                                                                       
 ::                                                                    
                                                                       
       pl2nvp ( &plane, n, p );                                      
                                                                       
 \`p' will be the closest point in the plane to the origin. The unit   
 normal vector \`n' will point from the origin toward the plane.       
 To find a point \`p' and two spanning vectors \`v1' and \`v2' that    
 define \`plane', use `pl2psv_c <../cspice/pl2psv_c.html>`__:          
                                                                       
 ::                                                                    
                                                                       
       pl2psv ( &plane, p, v1, v2 );                                 
                                                                       
 \`p' will be the closest point in the plane to the origin. The        
 vectors \`v1' and \`v2' are mutually orthogonal unit vectors and are  
 also orthogonal to \`p'.                                              
 It is important to note that the xxx2PL and PL2xxx routines are not   
 exact inverses of each other. The pairs of calls                      
                                                                       
 ::                                                                    
                                                                       
       nvc2pl ( n,      c,   &plane )                                
       pl2nvc ( &plane,  n,   &c    )                                
                                                                       
       nvp2pl ( p,      n,   &plane )                                
       pl2nvp ( plane   p,   n     )                                 
                                                                       
       psv2pl ( v1,     v2,  p,    &plane )                          
       pl2psv ( &plane, v1,  v2,   p      )                          
                                                                       
 do not necessarily preserve the input arguments supplied to the       
 xxx2PL routines. This is because the uniform internal representation  
 of SPICE planes causes them to \`forget' what data they were created  
 from; all sets of data that define the same geometric plane have the  
 same internal representation in SPICE planes.                         
 In general, the routines `pl2nvc_c <../cspice/pl2nvc_c.html>`__,      
 `pl2nvp_c <../cspice/pl2nvp_c.html>`__, and                           
 `pl2psv_c <../cspice/pl2psv_c.html>`__ are used in routines that      
 accept planes as input arguments. In this role, they simplify the     
 routines that call them, because the calling routines no longer check 
 the input planes' validity.                                           
                                                               
Examples                                                  
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                             
                                
                                                                       
Converting between representations of planes              
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                                            
 | The CSPICE plane routines can also be used as a convenient way to   
   convert one representation of a plane to another. For example,      
   suppose that given a normal vector \`n' and constant \`c' defining  
   a plane, you must produce the closest point in the plane to the     
   origin. The code fragment                                           
                                                                       
 ::                                                                    
                                                                       
       nvc2pl ( n,       c,  &plane );                               
       pl2nvp ( &plane,  n,  point  );                               
                                                                       
                                                
                                                                       
Translating planes                                        
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                                            
 | A \`translation' T is a vector space mapping defined by the         
   relation                                                            
                                                                       
 ::                                                                    
                                                                       
       T(X) = X + A   for all vectors X                                
                                                                       
 where A is a constant vector. While it's not difficult to directly    
 apply a translation map to a plane, using SPICE plane routines        
 provides the convenience of automatically computing the closest point 
 to the origin in the translated plane.                                
 Suppose a plane is defined by the point \`p' and the normal vector    
 \`n', and you wish to translate it by the vector \`x'. That is, you   
 wish to find data defining the plane that results from adding \`x' to 
 every vector in the original plane. You can do this with the code     
 fragment                                                              
                                                                       
 ::                                                                    
                                                                       
       vadd_c   ( p,      x, p      );              (Vector addition)  
       nvp2pl ( n,      p, &plane );                                 
       pl2nvp ( &plane, n, p      );                                 
                                                                       
 Now, \`p' is the closest point in the translated plane to the origin. 
                                
                                                                       
Applying linear transformations to planes                 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                                            
 | Suppose we have a normal vector N and constant C defining a plane,  
   and we wish to apply a non-singular linear transformation T to the  
   plane. We want to find a unit normal vector and constant that       
   define the transformed plane; the constant should be the distance   
   of the plane from the origin.                                       
                                                                       
 ::                                                                    
                                                                       
            Let T be represented by the matrix M.                      
                                                                       
            If Y is a point in the transformed plane, then             
                                                                       
                -1                                                     
               M   Y                                                   
                                                                       
            is a point in the original plane, so                       
                                                                       
                     -1                                                
               < N, M  Y >  =  C.                                      
                                                                       
            But                                                        
                                                                       
                     -1           T  -1                                
               < N, M  Y >  =    N  M   Y                              
                                                                       
                                      -1 T     T                       
                            =   (  ( M  )  N  )   Y                    
                                                                       
                                      -1 T                             
                            =   <  ( M  )  N,  Y >                     
                                                                       
            So                                                         
                                                                       
                  -1 T                                                 
               ( M  )  N,  C                                           
                                                                       
            are, respectively, a normal vector and constant for the    
            transformed plane.                                         
                                                                       
 We can solve the problem using the following code fragments.          
 Make a SPICE plane from \`n' and \`c', and then find a point in       
 \`plane' and spanning vectors for \`plane'. \`n' need not be a unit   
 vector.                                                               
                                                                       
 ::                                                                    
                                                                       
       nvc2pl ( n,      c,      &plane     )                         
       pl2psv ( &plane,  point,  v1,    v2 )                         
                                                                       
 Apply the linear transformation to the point and spanning vectors.    
 All we need to do is multiply these vectors by M, since for any       
 linear transformation T,                                              
 ::                                                                    
                                                                       
                  T ( POINT   +     t1 * V1     +   t2 * V2 )          
                                                                       
               =  T (POINT)   +   t1 * T (V1)   +   t2 * T (V2),       
                                                                       
 which means that T(POINT), T(V1), and T(V2) are a a point and         
 spanning vectors for the transformed plane.                           
 ::                                                                    
                                                                       
       mxv ( m, point, tpoint );                                     
       mxv ( m, v1,    tv1    );                                     
       mxv ( m, v2,    tv2    );                                     
                                                                       
 Construct a new SPICE plane \`tplane' from the transformed point and  
 spanning vectors, and find a unit normal and constant for this new    
 plane.                                                                
 ::                                                                    
                                                                       
       psv2pl ( tpoint,   tv1,  tv2,  &tplane );                     
       pl2nvc ( &tplane,   tn,   tc           );                     
                                                                       
                                                
                                                                       
Finding the limb of an ellipsoid                          
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                                            
 | This problem is somewhat artificial, because the SPICE routine      
   `edlimb_c <../cspice/edlimb_c.html>`__ already solves this problem. 
   Nonetheless, it is a good illustration of how CSPICE plane routines 
   are used.                                                           
                                                                       
 We'll work in body-fixed coordinates, which is to say that the        
 ellipsoid is centered at the origin and has axes aligned with the x,  
 y and z axes. Suppose that the semi-axes of the ellipsoid has lengths 
 A, B, and C, and call our observation point                           
                                                                       
 ::                                                                    
                                                                       
       P = ( p1, p2, p3 ).                                             
                                                                       
 Then every point                                                      
 ::                                                                    
                                                                       
       X = ( x1, x2, x3 )                                              
                                                                       
 on the limb satisfies                                                 
 ::                                                                    
                                                                       
       < P - X, N > = 0                                                
                                                                       
 where N a surface normal vector at X. In particular, the gradient     
 vector                                                                
 ::                                                                    
                                                                       
             2      2      2                                           
       ( x1/A , x2/B , x3/C  )                                         
                                                                       
 is a surface normal, so X satisfies                                   
 ::                                                                    
                                                                       
       0 = < P - X, N >                                                
                                                                       
                         2      2      2                               
         = < P - X, (x1/A , x2/B , x3/C ) >                            
                                                                       
                     2      2      2                  2      2      2  
                                                                       
       = < P, (x1/A , x2/B , x3/C ) >  -  < X, (x1/A , x2/B , x3/C ) > 
                                                                       
                  2      2      2                                      
         = < (p1/A , p2/B , p3/C ), X >  -  1                          
                                                                       
 So the limb plane has normal vector                                   
 ::                                                                    
                                                                       
                 2      2      2                                       
       N = ( p1/A , p2/B , p3/C  )                                     
                                                                       
 and constant 1. We can create a SPICE plane representing the limb     
 with the code fragment                                                
 ::                                                                    
                                                                       
       n(0) = p(0) / pow(a,2)                                          
       n(1) = p(1) / pow(b,2)                                          
       n(2) = p(2) / pow(c,2)                                          
                                                                       
       nvc2pl ( n, 1., &plane );                                     
                                                                       
 The limb is the intersection of the limb plane and the ellipsoid. To  
 find the intersection, we use the CSPICE routine                      
 `inedpl_c <../cspice/inedpl_c.html>`__ (Intersection of ellipsoid and 
 plane):                                                               
 ::                                                                    
                                                                       
       inedpl ( a,  b,  c,  &plane, &ellips, &found );               
                                                                       
 \`ellips' is a SPICE \`ellipse', a data type analogous to the SPICE   
 plane. We can use the CSPICE routine                                  
 `el2cgv_c <../cspice/el2cgv_c.html>`__ (Ellipse to center and         
 generating vectors) to find the limb's center, semi-major axis, and   
 semi-minor axis:                                                      
 ::                                                                    
                                                                       
       el2cgv ( &ellips, center, smajor, sminor );                   
                                                                       
                                                
                                                                       
Header examples                                           
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                                            
 | The headers of the plane routines (see                              
   `planes.req <../req/planes.html>`__) list additional ellipse usage  
   examples.                                                           
                                                               
Use of ellipses with planes                               
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                                            
 | The nature of geometry problems involving planes often includes use 
   of the SPICE ellipse data type. The example code listed in the      
   headers of the routines `inelpl_c <../cspice/inelpl_c.html>`__ and  
   `pjelpl_c <../cspice/pjelpl_c.html>`__ show examples of problems    
   solved using both the ellipse and plane data type.                  
                                                               
Summary of routines                                       
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                                  
 | The following table summarizes the CSPICE plane routines.           
                                                                       
 ::                                                                    
                                                                       
       inedpl            Intersection of ellipsoid and plane        
       inelpl            Intersection of ellipse and plane          
       inrypl            Intersection of ray and plane              
       nvc2pl            Normal vector and constant to plane        
       nvp2pl            Normal vector and point to plane           
       pjelpl            Project ellipse onto plane                 
       pl2nvc            Plane to normal vector and constant      
       pl2nvp            Plane to normal vector and point           
       pl2psv            Plane to point and spanning vectors        
       psv2pl            Point and spanning vectors to plane        
       vprjp             Vector projection onto plane               
       vprjpi            Vector projection onto plane, inverted     
                                                                       

