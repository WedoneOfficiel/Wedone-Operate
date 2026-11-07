#version 440

layout(location = 0) in vec2 qt_TexCoord0;
layout(location = 0) out vec4 fragColor;
layout(binding = 1) uniform sampler2D source;

layout(std140, binding = 0) uniform buf {
    mat4 qt_Matrix;
    float qt_Opacity;
    vec2 texelSize;
    vec2 itemSize;
    float radius;
    float refractionStrength;
    float blur;
    vec4 glassTint;
    float opacityFactor;
    vec2 lightPosition;
    float pointerIntensity;
} ubuf;

float roundedBoxDistance(vec2 point, vec2 halfSize, float cornerRadius)
{
    vec2 q = abs(point) - halfSize + vec2(cornerRadius);
    return length(max(q, vec2(0.0))) + min(max(q.x, q.y), 0.0) - cornerRadius;
}

void main()
{
    vec2 uv = qt_TexCoord0;
    vec2 pixel = uv * ubuf.itemSize;
    vec2 centered = pixel - ubuf.itemSize * 0.5;
    float distanceToEdge = roundedBoxDistance(
        centered, ubuf.itemSize * 0.5,
        min(ubuf.radius, min(ubuf.itemSize.x, ubuf.itemSize.y) * 0.5)
    );

    float inside = 1.0 - smoothstep(-0.8, 0.8, distanceToEdge);
    float edge = 1.0 - smoothstep(-5.0, -0.2, distanceToEdge);
    vec2 normal = normalize(centered + vec2(0.001, 0.001));
    vec2 displacement = normal * ubuf.texelSize * ubuf.refractionStrength * edge;

    float blurPixels = max(0.0, ubuf.blur);
    vec3 base = texture(source, uv + displacement).rgb * 0.40;
    base += texture(source, uv + displacement + vec2(ubuf.texelSize.x * blurPixels, 0.0)).rgb * 0.15;
    base += texture(source, uv + displacement - vec2(ubuf.texelSize.x * blurPixels, 0.0)).rgb * 0.15;
    base += texture(source, uv + displacement + vec2(0.0, ubuf.texelSize.y * blurPixels)).rgb * 0.15;
    base += texture(source, uv + displacement - vec2(0.0, ubuf.texelSize.y * blurPixels)).rgb * 0.15;

    float tintAmount = clamp(ubuf.glassTint.a * ubuf.opacityFactor, 0.0, 1.0);
    vec3 color = mix(base, ubuf.glassTint.rgb, tintAmount);
    float topSheen = pow(1.0 - smoothstep(0.0, 0.48, uv.y), 2.0) * 0.13;
    float rim = (1.0 - smoothstep(0.0, 1.8, abs(distanceToEdge))) * 0.22;
    float fresnel = pow(1.0 - max(dot(normalize(vec3(centered, 80.0)), vec3(0.0, 0.0, 1.0)), 0.0), 2.0) * edge;
    vec2 lightDelta = (pixel - ubuf.lightPosition) / max(1.0, min(ubuf.itemSize.x, ubuf.itemSize.y));
    float cursorSpecular = exp(-dot(lightDelta, lightDelta) * 54.0) * ubuf.pointerIntensity * 0.18;
    color += vec3(1.0) * (topSheen + rim + fresnel * 0.12 + cursorSpecular);
    fragColor = vec4(color, inside * ubuf.qt_Opacity);
}
