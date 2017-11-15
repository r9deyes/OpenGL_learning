layout(location=0) in vec3 VertexPosition;
layout(location=1) in vec3 VertexColor;
out vec4 Color;
uniform mat4 RotationMatrix;
void main()
{
    Color = vec4(VertexColor,1.0);
    gl_Position= vec4(VertexPosition,1.0) * RotationMatrix ;
}