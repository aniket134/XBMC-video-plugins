xof 0302txt 0064

// Created by AC3D 6.0.30 ( www.ac3d.org )
// Export Plugin : 'DirectX.p' v1.9 by Frank Meinert


Material MatTex_5_0 {
  1.0; 1.0; 0.0; 1.0;;
  16.0;
  0.2; 0.2; 0.2;;
  0.0; 0.0; 0.0;;
}

Material MatTex_12_0 {
  0.266667; 0.266667; 0.266667; 1.0;;
  16.0;
  0.2; 0.2; 0.2;;
  0.0; 0.0; 0.0;;
}

Material MatTex_1_1 {
  1.0; 1.0; 1.0; 1.0;;
  16.0;
  0.2; 0.2; 0.2;;
  0.0; 0.0; 0.0;;
  TextureFileName { "hockeysurface.png"; }
}


Frame WORLD {

FrameTransformMatrix {
  1.0, 0.0, 0.0, 0.0,
  0.0, 1.0, 0.0, 0.0,
  0.0, 0.0, 1.0, 0.0,
  0.0, 0.0, 0.0, 1.0;;
}

Frame goal2 {

FrameTransformMatrix {
  1.0, 0.0, 0.0, 0.0,
  0.0, 1.0, 0.0, 0.0,
  0.0, 0.0, 1.0, 0.0,
  0.0, 0.0, -42.5, 1.0;;
}

Mesh goal2 {
40;
-9.0;1.5;2.5;,
-9.0;-1.5;2.5;,
-9.0;-1.5;-2.5;,
-9.0;1.5;-2.5;,
-9.0;1.5;-2.5;,
-9.0;-1.5;-2.5;,
-9.0;-1.5;2.5;,
-9.0;1.5;2.5;,
9.0;1.5;-2.5;,
9.0;-1.5;-2.5;,
9.0;-1.5;2.5;,
9.0;1.5;2.5;,
9.0;1.5;2.5;,
9.0;-1.5;2.5;,
9.0;-1.5;-2.5;,
9.0;1.5;-2.5;,
-9.0;1.5;-2.5;,
-9.0;-1.5;-2.5;,
9.0;-1.5;-2.5;,
9.0;1.5;-2.5;,
9.0;1.5;-2.5;,
9.0;-1.5;-2.5;,
-9.0;-1.5;-2.5;,
-9.0;1.5;-2.5;,
9.0;1.5;-2.5;,
9.0;1.5;2.5;,
-9.0;1.5;2.5;,
-9.0;1.5;-2.5;,
-9.0;1.5;-2.5;,
-9.0;1.5;2.5;,
9.0;1.5;2.5;,
9.0;1.5;-2.5;,
9.0;-1.5;-2.5;,
-9.0;-1.5;-2.5;,
-9.0;-1.5;2.5;,
9.0;-1.5;2.5;,
9.0;-1.5;2.5;,
-9.0;-1.5;2.5;,
-9.0;-1.5;-2.5;,
9.0;-1.5;-2.5;;

10;
4;0,1,2,3;,
4;4,5,6,7;,
4;8,9,10,11;,
4;12,13,14,15;,
4;16,17,18,19;,
4;20,21,22,23;,
4;24,25,26,27;,
4;28,29,30,31;,
4;32,33,34,35;,
4;36,37,38,39;;

MeshMaterialList {
1;
10;
0,
0,
0,
0,
0,
0,
0,
0,
0,
0;;
{ MatTex_5_0 }
}

MeshNormals{
40;
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;;

10;
4;0,1,2,3;,
4;4,5,6,7;,
4;8,9,10,11;,
4;12,13,14,15;,
4;16,17,18,19;,
4;20,21,22,23;,
4;24,25,26,27;,
4;28,29,30,31;,
4;32,33,34,35;,
4;36,37,38,39;;
}


}

}

Frame CSG0 {

FrameTransformMatrix {
  1.0, 0.0, 0.0, 0.0,
  0.0, 1.0, 0.0, 0.0,
  0.0, 0.0, 1.0, 0.0,
  0.124257, 0.166221, 78.9483, 1.0;;
}

Mesh CSG0 {
159;
8.0;0.446253;-38.9483;,
21.9629;0.5;-38.9483;,
8.0;0.5;-38.9483;,
8.0;0.446253;-38.9483;,
8.0;0.260921;-38.9483;,
21.9629;0.5;-38.9483;,
21.9629;-0.253384;-38.9483;,
21.9629;0.5;-38.9483;,
8.0;0.260921;-38.9483;,
8.0;0.260921;-38.9483;,
8.0;-0.14138;-38.9483;,
21.9629;-0.253384;-38.9483;,
8.0;-0.14138;-38.9483;,
8.0;-0.253384;-38.9483;,
21.9629;-0.253384;-38.9483;,
8.0;0.097698;-39.9483;,
8.0;0.381292;-39.9483;,
21.9629;-0.253384;-39.9483;,
8.0;-0.014305;-39.9483;,
8.0;0.097698;-39.9483;,
21.9629;-0.253384;-39.9483;,
8.0;-0.253384;-39.9483;,
8.0;-0.014305;-39.9483;,
21.9629;-0.253384;-39.9483;,
21.9629;0.5;-39.9483;,
21.9629;-0.253384;-39.9483;,
8.0;0.381292;-39.9483;,
8.0;0.381292;-39.9483;,
8.0;0.5;-39.9483;,
21.9629;0.5;-39.9483;,
8.0;-0.253384;-39.4823;,
8.0;-0.253384;-39.631;,
21.9629;-0.253384;-39.9483;,
8.0;-0.253384;-38.9483;,
8.0;-0.253384;-39.4823;,
21.9629;-0.253384;-39.9483;,
21.9629;-0.253384;-38.9483;,
8.0;-0.253384;-38.9483;,
21.9629;-0.253384;-39.9483;,
8.0;-0.253384;-39.9483;,
21.9629;-0.253384;-39.9483;,
8.0;-0.253384;-39.631;,
-22.0371;0.5;-38.9483;,
-22.0371;-0.253384;-38.9483;,
-8.0;0.384665;-38.9483;,
-8.0;0.384665;-38.9483;,
-8.0;0.5;-38.9483;,
-22.0371;0.5;-38.9483;,
-8.0;-0.013034;-38.9483;,
-8.0;0.384665;-38.9483;,
-22.0371;-0.253384;-38.9483;,
-8.0;-0.253384;-38.9483;,
-8.0;-0.013034;-38.9483;,
-22.0371;-0.253384;-38.9483;,
-8.0;0.259651;-39.9483;,
-22.0371;0.5;-39.9483;,
-8.0;0.5;-39.9483;,
-22.0371;-0.253384;-39.9483;,
-22.0371;0.5;-39.9483;,
-8.0;0.259651;-39.9483;,
-8.0;0.259651;-39.9483;,
-8.0;-0.253384;-39.9483;,
-22.0371;-0.253384;-39.9483;,
-8.0;-0.253384;-38.9483;,
-22.0371;-0.253384;-38.9483;,
-8.0;-0.253384;-39.2673;,
-8.0;-0.253384;-39.9483;,
-8.0;-0.253384;-39.2673;,
-22.0371;-0.253384;-38.9483;,
-22.0371;-0.253384;-39.9483;,
-8.0;-0.253384;-39.9483;,
-22.0371;-0.253384;-38.9483;,
-22.0371;0.5;-38.9483;,
-5.46264;0.5;-38.9483;,
21.9629;1.74661;-38.9483;,
-22.0371;1.74661;-38.9483;,
-22.0371;0.5;-38.9483;,
21.9629;1.74661;-38.9483;,
21.9629;0.5;-38.9483;,
21.9629;1.74661;-38.9483;,
-5.46264;0.5;-38.9483;,
-22.0371;0.5;-39.9483;,
-22.0371;1.74661;-39.9483;,
5.38845;0.5;-39.9483;,
21.9629;0.5;-39.9483;,
5.38845;0.5;-39.9483;,
-22.0371;1.74661;-39.9483;,
21.9629;1.74661;-39.9483;,
21.9629;0.5;-39.9483;,
-22.0371;1.74661;-39.9483;,
21.9629;1.74661;-38.9483;,
21.9629;-0.253384;-38.9483;,
21.9629;-0.253384;-39.9483;,
21.9629;1.74661;-39.9483;,
21.9629;1.74661;-38.9483;,
21.9629;-0.253384;-38.9483;,
21.9629;-0.253384;-39.9483;,
21.9629;1.74661;-39.9483;,
-22.0371;1.74661;-39.9483;,
-22.0371;-0.253384;-39.9483;,
-22.0371;-0.253384;-38.9483;,
-22.0371;1.74661;-38.9483;,
-22.0371;1.74661;-39.9483;,
-22.0371;-0.253384;-39.9483;,
-22.0371;-0.253384;-38.9483;,
-22.0371;1.74661;-38.9483;,
21.9629;1.74661;-38.9483;,
21.9629;1.74661;-39.9483;,
-22.0371;1.74661;-39.9483;,
-22.0371;1.74661;-38.9483;,
21.9629;1.74661;-38.9483;,
21.9629;1.74661;-39.9483;,
-22.0371;1.74661;-39.9483;,
-22.0371;1.74661;-38.9483;,
8.0;-0.22415;-39.9483;,
8.0;-0.253384;-39.9483;,
8.0;0.27585;-38.9483;,
8.0;0.266802;-38.9483;,
8.0;0.27585;-38.9483;,
8.0;-0.253384;-39.9483;,
8.0;-0.253384;-39.9483;,
8.0;-0.253384;-38.9483;,
8.0;0.266802;-38.9483;,
8.0;0.27585;-38.9483;,
8.0;0.5;-38.9483;,
8.0;-0.22415;-39.9483;,
8.0;0.5;-38.9483;,
8.0;0.5;-39.9483;,
8.0;-0.22415;-39.9483;,
-8.0;-0.253384;-38.9932;,
-8.0;-0.253384;-39.9483;,
-8.0;0.22415;-39.9483;,
-8.0;0.22415;-39.9483;,
-8.0;0.5;-39.9483;,
-8.0;-0.253384;-38.9932;,
-8.0;0.5;-39.9483;,
-8.0;0.5;-38.9483;,
-8.0;-0.253384;-38.9932;,
-8.0;0.5;-38.9483;,
-8.0;-0.184752;-38.9483;,
-8.0;-0.253384;-38.9932;,
-8.0;-0.253384;-38.9932;,
-8.0;-0.184752;-38.9483;,
-8.0;-0.253384;-38.9483;,
4.4136;0.5;-38.9483;,
-6.63383;0.5;-38.9483;,
-3.5864;0.5;-39.9483;,
-8.0;0.5;-39.9483;,
-3.5864;0.5;-39.9483;,
-8.0;0.5;-38.9483;,
-6.63383;0.5;-38.9483;,
-8.0;0.5;-38.9483;,
-3.5864;0.5;-39.9483;,
-3.5864;0.5;-39.9483;,
8.0;0.5;-39.9483;,
4.4136;0.5;-38.9483;,
8.0;0.5;-38.9483;,
4.4136;0.5;-38.9483;,
8.0;0.5;-39.9483;;

51;
3;0,1,2;,
3;3,4,5;,
3;6,7,8;,
3;9,10,11;,
3;12,13,14;,
3;15,16,17;,
3;18,19,20;,
3;21,22,23;,
3;24,25,26;,
3;27,28,29;,
3;30,31,32;,
3;33,34,35;,
3;36,37,38;,
3;39,40,41;,
3;42,43,44;,
3;45,46,47;,
3;48,49,50;,
3;51,52,53;,
3;54,55,56;,
3;57,58,59;,
3;60,61,62;,
3;63,64,65;,
3;66,67,68;,
3;69,70,71;,
3;72,73,74;,
3;75,76,77;,
3;78,79,80;,
3;81,82,83;,
3;84,85,86;,
3;87,88,89;,
4;90,91,92,93;,
4;94,95,96,97;,
4;98,99,100,101;,
4;102,103,104,105;,
4;106,107,108,109;,
4;110,111,112,113;,
3;114,115,116;,
3;117,118,119;,
3;120,121,122;,
3;123,124,125;,
3;126,127,128;,
3;129,130,131;,
3;132,133,134;,
3;135,136,137;,
3;138,139,140;,
3;141,142,143;,
3;144,145,146;,
3;147,148,149;,
3;150,151,152;,
3;153,154,155;,
3;156,157,158;;

MeshMaterialList {
1;
51;
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0;;
{ MatTex_12_0 }
}

MeshNormals{
159;
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;;

51;
3;0,1,2;,
3;3,4,5;,
3;6,7,8;,
3;9,10,11;,
3;12,13,14;,
3;15,16,17;,
3;18,19,20;,
3;21,22,23;,
3;24,25,26;,
3;27,28,29;,
3;30,31,32;,
3;33,34,35;,
3;36,37,38;,
3;39,40,41;,
3;42,43,44;,
3;45,46,47;,
3;48,49,50;,
3;51,52,53;,
3;54,55,56;,
3;57,58,59;,
3;60,61,62;,
3;63,64,65;,
3;66,67,68;,
3;69,70,71;,
3;72,73,74;,
3;75,76,77;,
3;78,79,80;,
3;81,82,83;,
3;84,85,86;,
3;87,88,89;,
4;90,91,92,93;,
4;94,95,96,97;,
4;98,99,100,101;,
4;102,103,104,105;,
4;106,107,108,109;,
4;110,111,112,113;,
3;114,115,116;,
3;117,118,119;,
3;120,121,122;,
3;123,124,125;,
3;126,127,128;,
3;129,130,131;,
3;132,133,134;,
3;135,136,137;,
3;138,139,140;,
3;141,142,143;,
3;144,145,146;,
3;147,148,149;,
3;150,151,152;,
3;153,154,155;,
3;156,157,158;;
}


}

}

Frame leg4 {

FrameTransformMatrix {
  1.0, 0.0, 0.0, 0.0,
  0.0, 1.0, 0.0, 0.0,
  0.0, 0.0, 1.0, 0.0,
  20.454, -15.2536, 37.4921, 1.0;;
}

Mesh leg4 {
48;
-1.5;15.0;-1.5;,
-1.5;-15.0;-1.5;,
1.5;-15.0;-1.5;,
1.5;15.0;-1.5;,
1.5;15.0;-1.5;,
1.5;-15.0;-1.5;,
-1.5;-15.0;-1.5;,
-1.5;15.0;-1.5;,
1.5;15.0;1.5;,
1.5;-15.0;1.5;,
-1.5;-15.0;1.5;,
-1.5;15.0;1.5;,
-1.5;15.0;1.5;,
-1.5;-15.0;1.5;,
1.5;-15.0;1.5;,
1.5;15.0;1.5;,
1.5;15.0;-1.5;,
1.5;-15.0;-1.5;,
1.5;-15.0;1.5;,
1.5;15.0;1.5;,
1.5;15.0;1.5;,
1.5;-15.0;1.5;,
1.5;-15.0;-1.5;,
1.5;15.0;-1.5;,
-1.5;15.0;1.5;,
-1.5;-15.0;1.5;,
-1.5;-15.0;-1.5;,
-1.5;15.0;-1.5;,
-1.5;15.0;-1.5;,
-1.5;-15.0;-1.5;,
-1.5;-15.0;1.5;,
-1.5;15.0;1.5;,
1.5;15.0;1.5;,
-1.5;15.0;1.5;,
-1.5;15.0;-1.5;,
1.5;15.0;-1.5;,
1.5;15.0;-1.5;,
-1.5;15.0;-1.5;,
-1.5;15.0;1.5;,
1.5;15.0;1.5;,
1.5;-15.0;1.5;,
1.5;-15.0;-1.5;,
-1.5;-15.0;-1.5;,
-1.5;-15.0;1.5;,
-1.5;-15.0;1.5;,
-1.5;-15.0;-1.5;,
1.5;-15.0;-1.5;,
1.5;-15.0;1.5;;

12;
4;0,1,2,3;,
4;4,5,6,7;,
4;8,9,10,11;,
4;12,13,14,15;,
4;16,17,18,19;,
4;20,21,22,23;,
4;24,25,26,27;,
4;28,29,30,31;,
4;32,33,34,35;,
4;36,37,38,39;,
4;40,41,42,43;,
4;44,45,46,47;;

MeshMaterialList {
1;
12;
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0;;
{ MatTex_12_0 }
}

MeshNormals{
48;
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;;

12;
4;0,1,2,3;,
4;4,5,6,7;,
4;8,9,10,11;,
4;12,13,14,15;,
4;16,17,18,19;,
4;20,21,22,23;,
4;24,25,26,27;,
4;28,29,30,31;,
4;32,33,34,35;,
4;36,37,38,39;,
4;40,41,42,43;,
4;44,45,46,47;;
}


}

}

Frame leg2 {

FrameTransformMatrix {
  1.0, 0.0, 0.0, 0.0,
  0.0, 1.0, 0.0, 0.0,
  0.0, 0.0, 1.0, 0.0,
  -20.4255, -15.3407, 37.4921, 1.0;;
}

Mesh leg2 {
48;
1.5;-15.0;1.5;,
1.5;-15.0;-1.5;,
-1.5;-15.0;-1.5;,
-1.5;-15.0;1.5;,
-1.5;-15.0;1.5;,
-1.5;-15.0;-1.5;,
1.5;-15.0;-1.5;,
1.5;-15.0;1.5;,
1.5;15.0;1.5;,
-1.5;15.0;1.5;,
-1.5;15.0;-1.5;,
1.5;15.0;-1.5;,
1.5;15.0;-1.5;,
-1.5;15.0;-1.5;,
-1.5;15.0;1.5;,
1.5;15.0;1.5;,
-1.5;15.0;1.5;,
-1.5;-15.0;1.5;,
-1.5;-15.0;-1.5;,
-1.5;15.0;-1.5;,
-1.5;15.0;-1.5;,
-1.5;-15.0;-1.5;,
-1.5;-15.0;1.5;,
-1.5;15.0;1.5;,
1.5;15.0;-1.5;,
1.5;-15.0;-1.5;,
1.5;-15.0;1.5;,
1.5;15.0;1.5;,
1.5;15.0;1.5;,
1.5;-15.0;1.5;,
1.5;-15.0;-1.5;,
1.5;15.0;-1.5;,
1.5;15.0;1.5;,
1.5;-15.0;1.5;,
-1.5;-15.0;1.5;,
-1.5;15.0;1.5;,
-1.5;15.0;1.5;,
-1.5;-15.0;1.5;,
1.5;-15.0;1.5;,
1.5;15.0;1.5;,
-1.5;15.0;-1.5;,
-1.5;-15.0;-1.5;,
1.5;-15.0;-1.5;,
1.5;15.0;-1.5;,
1.5;15.0;-1.5;,
1.5;-15.0;-1.5;,
-1.5;-15.0;-1.5;,
-1.5;15.0;-1.5;;

12;
4;0,1,2,3;,
4;4,5,6,7;,
4;8,9,10,11;,
4;12,13,14,15;,
4;16,17,18,19;,
4;20,21,22,23;,
4;24,25,26,27;,
4;28,29,30,31;,
4;32,33,34,35;,
4;36,37,38,39;,
4;40,41,42,43;,
4;44,45,46,47;;

MeshMaterialList {
1;
12;
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0;;
{ MatTex_12_0 }
}

MeshNormals{
48;
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;;

12;
4;0,1,2,3;,
4;4,5,6,7;,
4;8,9,10,11;,
4;12,13,14,15;,
4;16,17,18,19;,
4;20,21,22,23;,
4;24,25,26,27;,
4;28,29,30,31;,
4;32,33,34,35;,
4;36,37,38,39;,
4;40,41,42,43;,
4;44,45,46,47;;
}


}

}

Frame leg3 {

FrameTransformMatrix {
  1.0, 0.0, 0.0, 0.0,
  0.0, 1.0, 0.0, 0.0,
  0.0, 0.0, 1.0, 0.0,
  20.3898, -15.1908, -38.5, 1.0;;
}

Mesh leg3 {
48;
1.5;-15.0;-1.5;,
-1.5;-15.0;-1.5;,
-1.5;-15.0;1.5;,
1.5;-15.0;1.5;,
1.5;-15.0;1.5;,
-1.5;-15.0;1.5;,
-1.5;-15.0;-1.5;,
1.5;-15.0;-1.5;,
1.5;15.0;-1.5;,
1.5;15.0;1.5;,
-1.5;15.0;1.5;,
-1.5;15.0;-1.5;,
-1.5;15.0;-1.5;,
-1.5;15.0;1.5;,
1.5;15.0;1.5;,
1.5;15.0;-1.5;,
1.5;15.0;1.5;,
1.5;-15.0;1.5;,
-1.5;-15.0;1.5;,
-1.5;15.0;1.5;,
-1.5;15.0;1.5;,
-1.5;-15.0;1.5;,
1.5;-15.0;1.5;,
1.5;15.0;1.5;,
-1.5;15.0;-1.5;,
-1.5;-15.0;-1.5;,
1.5;-15.0;-1.5;,
1.5;15.0;-1.5;,
1.5;15.0;-1.5;,
1.5;-15.0;-1.5;,
-1.5;-15.0;-1.5;,
-1.5;15.0;-1.5;,
1.5;15.0;-1.5;,
1.5;-15.0;-1.5;,
1.5;-15.0;1.5;,
1.5;15.0;1.5;,
1.5;15.0;1.5;,
1.5;-15.0;1.5;,
1.5;-15.0;-1.5;,
1.5;15.0;-1.5;,
-1.5;15.0;1.5;,
-1.5;-15.0;1.5;,
-1.5;-15.0;-1.5;,
-1.5;15.0;-1.5;,
-1.5;15.0;-1.5;,
-1.5;-15.0;-1.5;,
-1.5;-15.0;1.5;,
-1.5;15.0;1.5;;

12;
4;0,1,2,3;,
4;4,5,6,7;,
4;8,9,10,11;,
4;12,13,14,15;,
4;16,17,18,19;,
4;20,21,22,23;,
4;24,25,26,27;,
4;28,29,30,31;,
4;32,33,34,35;,
4;36,37,38,39;,
4;40,41,42,43;,
4;44,45,46,47;;

MeshMaterialList {
1;
12;
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0;;
{ MatTex_12_0 }
}

MeshNormals{
48;
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;;

12;
4;0,1,2,3;,
4;4,5,6,7;,
4;8,9,10,11;,
4;12,13,14,15;,
4;16,17,18,19;,
4;20,21,22,23;,
4;24,25,26,27;,
4;28,29,30,31;,
4;32,33,34,35;,
4;36,37,38,39;,
4;40,41,42,43;,
4;44,45,46,47;;
}


}

}

Frame box2 {

FrameTransformMatrix {
  1.0, 0.0, 0.0, 0.0,
  0.0, 1.0, 0.0, 0.0,
  0.0, 0.0, 1.0, 0.0,
  21.5038, 0.912837, 0.0, 1.0;;
}

Mesh box2 {
48;
0.5;1.0;-39.0;,
0.5;-1.0;-39.0;,
0.5;-1.0;39.0;,
0.5;1.0;39.0;,
0.5;1.0;39.0;,
0.5;-1.0;39.0;,
0.5;-1.0;-39.0;,
0.5;1.0;-39.0;,
-0.5;1.0;39.0;,
-0.5;-1.0;39.0;,
-0.5;-1.0;-39.0;,
-0.5;1.0;-39.0;,
-0.5;1.0;-39.0;,
-0.5;-1.0;-39.0;,
-0.5;-1.0;39.0;,
-0.5;1.0;39.0;,
0.5;1.0;39.0;,
0.5;-1.0;39.0;,
-0.5;-1.0;39.0;,
-0.5;1.0;39.0;,
-0.5;1.0;39.0;,
-0.5;-1.0;39.0;,
0.5;-1.0;39.0;,
0.5;1.0;39.0;,
-0.5;1.0;-39.0;,
-0.5;-1.0;-39.0;,
0.5;-1.0;-39.0;,
0.5;1.0;-39.0;,
0.5;1.0;-39.0;,
0.5;-1.0;-39.0;,
-0.5;-1.0;-39.0;,
-0.5;1.0;-39.0;,
-0.5;1.0;39.0;,
-0.5;1.0;-39.0;,
0.5;1.0;-39.0;,
0.5;1.0;39.0;,
0.5;1.0;39.0;,
0.5;1.0;-39.0;,
-0.5;1.0;-39.0;,
-0.5;1.0;39.0;,
-0.5;-1.0;39.0;,
0.5;-1.0;39.0;,
0.5;-1.0;-39.0;,
-0.5;-1.0;-39.0;,
-0.5;-1.0;-39.0;,
0.5;-1.0;-39.0;,
0.5;-1.0;39.0;,
-0.5;-1.0;39.0;;

12;
4;0,1,2,3;,
4;4,5,6,7;,
4;8,9,10,11;,
4;12,13,14,15;,
4;16,17,18,19;,
4;20,21,22,23;,
4;24,25,26,27;,
4;28,29,30,31;,
4;32,33,34,35;,
4;36,37,38,39;,
4;40,41,42,43;,
4;44,45,46,47;;

MeshMaterialList {
1;
12;
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0;;
{ MatTex_12_0 }
}

MeshNormals{
48;
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;;

12;
4;0,1,2,3;,
4;4,5,6,7;,
4;8,9,10,11;,
4;12,13,14,15;,
4;16,17,18,19;,
4;20,21,22,23;,
4;24,25,26,27;,
4;28,29,30,31;,
4;32,33,34,35;,
4;36,37,38,39;,
4;40,41,42,43;,
4;44,45,46,47;;
}


}

}

Frame rect {

FrameTransformMatrix {
  1.0, 0.0, 0.0, 0.0,
  0.0, 1.0, 0.0, 0.0,
  0.0, 0.0, 1.0, 0.0,
  0.0, 0.0, 0.0, 1.0;;
}

Mesh rect {
8;
-21.0;0.0;39.0;,
-21.0;0.0;-39.0;,
21.0;0.0;-39.0;,
21.0;0.0;39.0;,
21.0;0.0;39.0;,
21.0;0.0;-39.0;,
-21.0;0.0;-39.0;,
-21.0;0.0;39.0;;

2;
4;0,1,2,3;,
4;4,5,6,7;;

MeshMaterialList {
1;
2;
0,
0;;
{ MatTex_1_1 }
}

MeshTextureCoords {
8;
0.0;0.0;,
0.0;1.0;,
1.0;1.0;,
1.0;0.0;,
1.0;0.0;,
1.0;1.0;,
0.0;1.0;,
0.0;0.0;;
}

MeshNormals{
8;
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;;

2;
4;0,1,2,3;,
4;4,5,6,7;;
}


}

}

Frame box3 {

FrameTransformMatrix {
  1.0, 0.0, 0.0, 0.0,
  0.0, 1.0, 0.0, 0.0,
  0.0, 0.0, 1.0, 0.0,
  -21.4128, 0.912837, 0.000001, 1.0;;
}

Mesh box3 {
48;
-0.5;-1.0;39.0;,
0.5;-1.0;39.0;,
0.5;-1.0;-39.0;,
-0.5;-1.0;-39.0;,
-0.5;-1.0;-39.0;,
0.5;-1.0;-39.0;,
0.5;-1.0;39.0;,
-0.5;-1.0;39.0;,
-0.5;1.0;39.0;,
-0.5;1.0;-39.0;,
0.5;1.0;-39.0;,
0.5;1.0;39.0;,
0.5;1.0;39.0;,
0.5;1.0;-39.0;,
-0.5;1.0;-39.0;,
-0.5;1.0;39.0;,
-0.5;1.0;-39.0;,
-0.5;-1.0;-39.0;,
0.5;-1.0;-39.0;,
0.5;1.0;-39.0;,
0.5;1.0;-39.0;,
0.5;-1.0;-39.0;,
-0.5;-1.0;-39.0;,
-0.5;1.0;-39.0;,
0.5;1.0;39.0;,
0.5;-1.0;39.0;,
-0.5;-1.0;39.0;,
-0.5;1.0;39.0;,
-0.5;1.0;39.0;,
-0.5;-1.0;39.0;,
0.5;-1.0;39.0;,
0.5;1.0;39.0;,
-0.5;1.0;39.0;,
-0.5;-1.0;39.0;,
-0.5;-1.0;-39.0;,
-0.5;1.0;-39.0;,
-0.5;1.0;-39.0;,
-0.5;-1.0;-39.0;,
-0.5;-1.0;39.0;,
-0.5;1.0;39.0;,
0.5;1.0;-39.0;,
0.5;-1.0;-39.0;,
0.5;-1.0;39.0;,
0.5;1.0;39.0;,
0.5;1.0;39.0;,
0.5;-1.0;39.0;,
0.5;-1.0;-39.0;,
0.5;1.0;-39.0;;

12;
4;0,1,2,3;,
4;4,5,6,7;,
4;8,9,10,11;,
4;12,13,14,15;,
4;16,17,18,19;,
4;20,21,22,23;,
4;24,25,26,27;,
4;28,29,30,31;,
4;32,33,34,35;,
4;36,37,38,39;,
4;40,41,42,43;,
4;44,45,46,47;;

MeshMaterialList {
1;
12;
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0;;
{ MatTex_12_0 }
}

MeshNormals{
48;
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;;

12;
4;0,1,2,3;,
4;4,5,6,7;,
4;8,9,10,11;,
4;12,13,14,15;,
4;16,17,18,19;,
4;20,21,22,23;,
4;24,25,26,27;,
4;28,29,30,31;,
4;32,33,34,35;,
4;36,37,38,39;,
4;40,41,42,43;,
4;44,45,46,47;;
}


}

}

Frame leg1 {

FrameTransformMatrix {
  1.0, 0.0, 0.0, 0.0,
  0.0, 1.0, 0.0, 0.0,
  0.0, 0.0, 1.0, 0.0,
  -20.4128, -15.1377, -38.5, 1.0;;
}

Mesh leg1 {
48;
-1.5;15.0;-1.5;,
-1.5;-15.0;-1.5;,
1.5;-15.0;-1.5;,
1.5;15.0;-1.5;,
1.5;15.0;-1.5;,
1.5;-15.0;-1.5;,
-1.5;-15.0;-1.5;,
-1.5;15.0;-1.5;,
1.5;15.0;1.5;,
1.5;-15.0;1.5;,
-1.5;-15.0;1.5;,
-1.5;15.0;1.5;,
-1.5;15.0;1.5;,
-1.5;-15.0;1.5;,
1.5;-15.0;1.5;,
1.5;15.0;1.5;,
1.5;15.0;-1.5;,
1.5;-15.0;-1.5;,
1.5;-15.0;1.5;,
1.5;15.0;1.5;,
1.5;15.0;1.5;,
1.5;-15.0;1.5;,
1.5;-15.0;-1.5;,
1.5;15.0;-1.5;,
-1.5;15.0;1.5;,
-1.5;-15.0;1.5;,
-1.5;-15.0;-1.5;,
-1.5;15.0;-1.5;,
-1.5;15.0;-1.5;,
-1.5;-15.0;-1.5;,
-1.5;-15.0;1.5;,
-1.5;15.0;1.5;,
1.5;15.0;1.5;,
-1.5;15.0;1.5;,
-1.5;15.0;-1.5;,
1.5;15.0;-1.5;,
1.5;15.0;-1.5;,
-1.5;15.0;-1.5;,
-1.5;15.0;1.5;,
1.5;15.0;1.5;,
1.5;-15.0;1.5;,
1.5;-15.0;-1.5;,
-1.5;-15.0;-1.5;,
-1.5;-15.0;1.5;,
-1.5;-15.0;1.5;,
-1.5;-15.0;-1.5;,
1.5;-15.0;-1.5;,
1.5;-15.0;1.5;;

12;
4;0,1,2,3;,
4;4,5,6,7;,
4;8,9,10,11;,
4;12,13,14,15;,
4;16,17,18,19;,
4;20,21,22,23;,
4;24,25,26,27;,
4;28,29,30,31;,
4;32,33,34,35;,
4;36,37,38,39;,
4;40,41,42,43;,
4;44,45,46,47;;

MeshMaterialList {
1;
12;
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0;;
{ MatTex_12_0 }
}

MeshNormals{
48;
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;;

12;
4;0,1,2,3;,
4;4,5,6,7;,
4;8,9,10,11;,
4;12,13,14,15;,
4;16,17,18,19;,
4;20,21,22,23;,
4;24,25,26,27;,
4;28,29,30,31;,
4;32,33,34,35;,
4;36,37,38,39;,
4;40,41,42,43;,
4;44,45,46,47;;
}


}

}

Frame CSG1 {

FrameTransformMatrix {
  1.0, 0.0, 0.0, 0.0,
  0.0, 1.0, 0.0, 0.0,
  0.0, 0.0, 1.0, 0.0,
  0.124257, 0.166221, -0.051696, 1.0;;
}

Mesh CSG1 {
159;
8.0;0.5;-38.9483;,
4.4136;0.5;-38.9483;,
8.0;0.5;-39.9483;,
-3.5864;0.5;-39.9483;,
8.0;0.5;-39.9483;,
4.4136;0.5;-38.9483;,
-6.63383;0.5;-38.9483;,
-8.0;0.5;-38.9483;,
-3.5864;0.5;-39.9483;,
-8.0;0.5;-39.9483;,
-3.5864;0.5;-39.9483;,
-8.0;0.5;-38.9483;,
4.4136;0.5;-38.9483;,
-6.63383;0.5;-38.9483;,
-3.5864;0.5;-39.9483;,
-8.0;-0.253384;-38.9932;,
-8.0;-0.184752;-38.9483;,
-8.0;-0.253384;-38.9483;,
-8.0;0.5;-38.9483;,
-8.0;-0.184752;-38.9483;,
-8.0;-0.253384;-38.9932;,
-8.0;0.5;-39.9483;,
-8.0;0.5;-38.9483;,
-8.0;-0.253384;-38.9932;,
-8.0;0.22415;-39.9483;,
-8.0;0.5;-39.9483;,
-8.0;-0.253384;-38.9932;,
-8.0;-0.253384;-38.9932;,
-8.0;-0.253384;-39.9483;,
-8.0;0.22415;-39.9483;,
8.0;0.5;-38.9483;,
8.0;0.5;-39.9483;,
8.0;-0.22415;-39.9483;,
8.0;0.27585;-38.9483;,
8.0;0.5;-38.9483;,
8.0;-0.22415;-39.9483;,
8.0;-0.253384;-39.9483;,
8.0;-0.253384;-38.9483;,
8.0;0.266801;-38.9483;,
8.0;0.266801;-38.9483;,
8.0;0.27585;-38.9483;,
8.0;-0.253384;-39.9483;,
8.0;-0.22415;-39.9483;,
8.0;-0.253384;-39.9483;,
8.0;0.27585;-38.9483;,
21.9629;1.74661;-38.9483;,
21.9629;1.74661;-39.9483;,
-22.0371;1.74661;-39.9483;,
-22.0371;1.74661;-38.9483;,
21.9629;1.74661;-38.9483;,
21.9629;1.74661;-39.9483;,
-22.0371;1.74661;-39.9483;,
-22.0371;1.74661;-38.9483;,
-22.0371;1.74661;-39.9483;,
-22.0371;-0.253384;-39.9483;,
-22.0371;-0.253384;-38.9483;,
-22.0371;1.74661;-38.9483;,
-22.0371;1.74661;-39.9483;,
-22.0371;-0.253384;-39.9483;,
-22.0371;-0.253384;-38.9483;,
-22.0371;1.74661;-38.9483;,
21.9629;1.74661;-38.9483;,
21.9629;-0.253384;-38.9483;,
21.9629;-0.253384;-39.9483;,
21.9629;1.74661;-39.9483;,
21.9629;1.74661;-38.9483;,
21.9629;-0.253384;-38.9483;,
21.9629;-0.253384;-39.9483;,
21.9629;1.74661;-39.9483;,
21.9629;1.74661;-39.9483;,
21.9629;0.5;-39.9483;,
-22.0371;1.74661;-39.9483;,
21.9629;0.5;-39.9483;,
5.38845;0.5;-39.9483;,
-22.0371;1.74661;-39.9483;,
-22.0371;0.5;-39.9483;,
-22.0371;1.74661;-39.9483;,
5.38845;0.5;-39.9483;,
21.9629;0.5;-38.9483;,
21.9629;1.74661;-38.9483;,
-5.46264;0.5;-38.9483;,
-22.0371;1.74661;-38.9483;,
-22.0371;0.5;-38.9483;,
21.9629;1.74661;-38.9483;,
-22.0371;0.5;-38.9483;,
-5.46264;0.5;-38.9483;,
21.9629;1.74661;-38.9483;,
-22.0371;-0.253384;-39.9483;,
-8.0;-0.253384;-39.9483;,
-22.0371;-0.253384;-38.9483;,
-8.0;-0.253384;-39.9483;,
-8.0;-0.253384;-39.2673;,
-22.0371;-0.253384;-38.9483;,
-8.0;-0.253384;-38.9483;,
-22.0371;-0.253384;-38.9483;,
-8.0;-0.253384;-39.2673;,
-8.0;0.259652;-39.9483;,
-8.0;-0.253384;-39.9483;,
-22.0371;-0.253384;-39.9483;,
-22.0371;-0.253384;-39.9483;,
-22.0371;0.5;-39.9483;,
-8.0;0.259652;-39.9483;,
-8.0;0.259652;-39.9483;,
-22.0371;0.5;-39.9483;,
-8.0;0.5;-39.9483;,
-8.0;-0.253384;-38.9483;,
-8.0;-0.013035;-38.9483;,
-22.0371;-0.253384;-38.9483;,
-8.0;-0.013035;-38.9483;,
-8.0;0.384665;-38.9483;,
-22.0371;-0.253384;-38.9483;,
-8.0;0.384665;-38.9483;,
-8.0;0.5;-38.9483;,
-22.0371;0.5;-38.9483;,
-22.0371;0.5;-38.9483;,
-22.0371;-0.253384;-38.9483;,
-8.0;0.384665;-38.9483;,
8.0;-0.253384;-39.9483;,
21.9629;-0.253384;-39.9483;,
8.0;-0.253384;-39.631;,
21.9629;-0.253384;-38.9483;,
8.0;-0.253384;-38.9483;,
21.9629;-0.253384;-39.9483;,
8.0;-0.253384;-38.9483;,
8.0;-0.253384;-39.4823;,
21.9629;-0.253384;-39.9483;,
8.0;-0.253384;-39.4823;,
8.0;-0.253384;-39.631;,
21.9629;-0.253384;-39.9483;,
8.0;0.381293;-39.9483;,
8.0;0.5;-39.9483;,
21.9629;0.5;-39.9483;,
21.9629;0.5;-39.9483;,
21.9629;-0.253384;-39.9483;,
8.0;0.381293;-39.9483;,
8.0;-0.253384;-39.9483;,
8.0;-0.014306;-39.9483;,
21.9629;-0.253384;-39.9483;,
8.0;-0.014306;-39.9483;,
8.0;0.097697;-39.9483;,
21.9629;-0.253384;-39.9483;,
8.0;0.097697;-39.9483;,
8.0;0.381293;-39.9483;,
21.9629;-0.253384;-39.9483;,
8.0;-0.14138;-38.9483;,
8.0;-0.253384;-38.9483;,
21.9629;-0.253384;-38.9483;,
8.0;0.260922;-38.9483;,
8.0;-0.14138;-38.9483;,
21.9629;-0.253384;-38.9483;,
21.9629;-0.253384;-38.9483;,
21.9629;0.5;-38.9483;,
8.0;0.260922;-38.9483;,
8.0;0.446253;-38.9483;,
8.0;0.260922;-38.9483;,
21.9629;0.5;-38.9483;,
8.0;0.446253;-38.9483;,
21.9629;0.5;-38.9483;,
8.0;0.5;-38.9483;;

51;
3;0,1,2;,
3;3,4,5;,
3;6,7,8;,
3;9,10,11;,
3;12,13,14;,
3;15,16,17;,
3;18,19,20;,
3;21,22,23;,
3;24,25,26;,
3;27,28,29;,
3;30,31,32;,
3;33,34,35;,
3;36,37,38;,
3;39,40,41;,
3;42,43,44;,
4;45,46,47,48;,
4;49,50,51,52;,
4;53,54,55,56;,
4;57,58,59,60;,
4;61,62,63,64;,
4;65,66,67,68;,
3;69,70,71;,
3;72,73,74;,
3;75,76,77;,
3;78,79,80;,
3;81,82,83;,
3;84,85,86;,
3;87,88,89;,
3;90,91,92;,
3;93,94,95;,
3;96,97,98;,
3;99,100,101;,
3;102,103,104;,
3;105,106,107;,
3;108,109,110;,
3;111,112,113;,
3;114,115,116;,
3;117,118,119;,
3;120,121,122;,
3;123,124,125;,
3;126,127,128;,
3;129,130,131;,
3;132,133,134;,
3;135,136,137;,
3;138,139,140;,
3;141,142,143;,
3;144,145,146;,
3;147,148,149;,
3;150,151,152;,
3;153,154,155;,
3;156,157,158;;

MeshMaterialList {
1;
51;
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0;;
{ MatTex_12_0 }
}

MeshNormals{
159;
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;;

51;
3;0,1,2;,
3;3,4,5;,
3;6,7,8;,
3;9,10,11;,
3;12,13,14;,
3;15,16,17;,
3;18,19,20;,
3;21,22,23;,
3;24,25,26;,
3;27,28,29;,
3;30,31,32;,
3;33,34,35;,
3;36,37,38;,
3;39,40,41;,
3;42,43,44;,
4;45,46,47,48;,
4;49,50,51,52;,
4;53,54,55,56;,
4;57,58,59,60;,
4;61,62,63,64;,
4;65,66,67,68;,
3;69,70,71;,
3;72,73,74;,
3;75,76,77;,
3;78,79,80;,
3;81,82,83;,
3;84,85,86;,
3;87,88,89;,
3;90,91,92;,
3;93,94,95;,
3;96,97,98;,
3;99,100,101;,
3;102,103,104;,
3;105,106,107;,
3;108,109,110;,
3;111,112,113;,
3;114,115,116;,
3;117,118,119;,
3;120,121,122;,
3;123,124,125;,
3;126,127,128;,
3;129,130,131;,
3;132,133,134;,
3;135,136,137;,
3;138,139,140;,
3;141,142,143;,
3;144,145,146;,
3;147,148,149;,
3;150,151,152;,
3;153,154,155;,
3;156,157,158;;
}


}

}

Frame goal1 {

FrameTransformMatrix {
  1.0, 0.0, 0.0, 0.0,
  0.0, 1.0, 0.0, 0.0,
  0.0, 0.0, 1.0, 0.0,
  0.000001, 0.0, 42.5, 1.0;;
}

Mesh goal1 {
40;
-9.0;-1.5;2.5;,
9.0;-1.5;2.5;,
9.0;-1.5;-2.5;,
-9.0;-1.5;-2.5;,
-9.0;-1.5;-2.5;,
9.0;-1.5;-2.5;,
9.0;-1.5;2.5;,
-9.0;-1.5;2.5;,
-9.0;1.5;2.5;,
-9.0;1.5;-2.5;,
9.0;1.5;-2.5;,
9.0;1.5;2.5;,
9.0;1.5;2.5;,
9.0;1.5;-2.5;,
-9.0;1.5;-2.5;,
-9.0;1.5;2.5;,
9.0;1.5;2.5;,
9.0;-1.5;2.5;,
-9.0;-1.5;2.5;,
-9.0;1.5;2.5;,
-9.0;1.5;2.5;,
-9.0;-1.5;2.5;,
9.0;-1.5;2.5;,
9.0;1.5;2.5;,
-9.0;1.5;2.5;,
-9.0;-1.5;2.5;,
-9.0;-1.5;-2.5;,
-9.0;1.5;-2.5;,
-9.0;1.5;-2.5;,
-9.0;-1.5;-2.5;,
-9.0;-1.5;2.5;,
-9.0;1.5;2.5;,
9.0;1.5;-2.5;,
9.0;-1.5;-2.5;,
9.0;-1.5;2.5;,
9.0;1.5;2.5;,
9.0;1.5;2.5;,
9.0;-1.5;2.5;,
9.0;-1.5;-2.5;,
9.0;1.5;-2.5;;

10;
4;0,1,2,3;,
4;4,5,6,7;,
4;8,9,10,11;,
4;12,13,14,15;,
4;16,17,18,19;,
4;20,21,22,23;,
4;24,25,26,27;,
4;28,29,30,31;,
4;32,33,34,35;,
4;36,37,38,39;;

MeshMaterialList {
1;
10;
0,
0,
0,
0,
0,
0,
0,
0,
0,
0;;
{ MatTex_5_0 }
}

MeshNormals{
40;
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;-1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;1.0;0.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;-1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
0.0;0.0;1.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
-1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;,
1.0;0.0;0.0;;

10;
4;0,1,2,3;,
4;4,5,6,7;,
4;8,9,10,11;,
4;12,13,14,15;,
4;16,17,18,19;,
4;20,21,22,23;,
4;24,25,26,27;,
4;28,29,30,31;,
4;32,33,34,35;,
4;36,37,38,39;;
}


}

}

}
