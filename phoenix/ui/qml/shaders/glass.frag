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

const float BEVEL_WIDTH = 10.0;
const float GLASS_IOR = 1.18;
const float DISPERSION = 0.018;

float roundedBoxDistance(vec2 point, vec2 halfSize, float cornerRadius)
{
    vec2 q = abs(point) - halfSize + vec2(cornerRadius);
    return length(max(q, vec2(0.0))) + min(max(q.x, q.y), 0.0) - cornerRadius;
}

vec3 sampleBackdrop(vec2 uv, vec2 offset, float blurRadius)
{
    vec2 stepX = vec2(ubuf.texelSize.x * blurRadius, 0.0);
    vec2 stepY = vec2(0.0, ubuf.texelSize.y * blurRadius);
    vec2 p = clamp(uv + offset, vec2(0.001), vec2(0.999));

    // Compact nine-tap Gaussian approximation. The centre retains most of
    // the scene detail; the surrounding samples soften it like thick glass.
    vec3 c = texture(source, p).rgb * 0.28;
    c += texture(source, clamp(p + stepX, vec2(0.001), vec2(0.999))).rgb * 0.12;
    c += texture(source, clamp(p - stepX, vec2(0.001), vec2(0.999))).rgb * 0.12;
    c += texture(source, clamp(p + stepY, vec2(0.001), vec2(0.999))).rgb * 0.12;
    c += texture(source, clamp(p - stepY, vec2(0.001), vec2(0.999))).rgb * 0.12;
    c += texture(source, clamp(p + stepX + stepY, vec2(0.001), vec2(0.999))).rgb * 0.06;
    c += texture(source, clamp(p - stepX + stepY, vec2(0.001), vec2(0.999))).rgb * 0.06;
    c += texture(source, clamp(p + stepX - stepY, vec2(0.001), vec2(0.999))).rgb * 0.06;
    c += texture(source, clamp(p - stepX - stepY, vec2(0.001), vec2(0.999))).rgb * 0.06;
    return c;
}

void main()
{
    vec2 uv = qt_TexCoord0;
    vec2 pixel = uv * ubuf.itemSize;
    vec2 centered = pixel - ubuf.itemSize * 0.5;
    float corner = min(ubuf.radius, min(ubuf.itemSize.x, ubuf.itemSize.y) * 0.5);
    float d = roundedBoxDistance(centered, ubuf.itemSize * 0.5, corner);

    float aa = max(fwidth(d), 0.75);
    float inside = 1.0 - smoothstep(-aa, aa, d);
    float edgeDistance = max(0.0, -d);
    float bevelT = clamp(edgeDistance / BEVEL_WIDTH, 0.0, 1.0);
    float bevel = 1.0 - smoothstep(0.0, 1.0, bevelT);

    // The SDF gradient gives the actual rounded-rectangle edge normal,
    // including the curved corners (unlike a radial-from-centre approximation).
    vec2 ex = vec2(1.0, 0.0);
    vec2 ey = vec2(0.0, 1.0);
    float dx = roundedBoxDistance(centered + ex, ubuf.itemSize * 0.5, corner)
             - roundedBoxDistance(centered - ex, ubuf.itemSize * 0.5, corner);
    float dy = roundedBoxDistance(centered + ey, ubuf.itemSize * 0.5, corner)
             - roundedBoxDistance(centered - ey, ubuf.itemSize * 0.5, corner);
    vec2 edgeNormal = normalize(vec2(dx, dy) + vec2(0.00001));

    // Approximate a rounded glass bevel as a changing surface normal, then
    // apply Snell's law to the view ray. A small RGB IOR split creates
    // restrained chromatic dispersion at the rim.
    float bevelSlope = (1.0 - smoothstep(0.0, BEVEL_WIDTH, edgeDistance)) * 0.72;
    vec3 surfaceNormal = normalize(vec3(edgeNormal * bevelSlope, 1.0));
    vec3 incident = vec3(0.0, 0.0, -1.0);
    float eta = 1.0 / GLASS_IOR;
    vec3 refracted = refract(incident, surfaceNormal, eta);
    vec2 rayShift = refracted.xy * (1.0 - bevelT) * ubuf.refractionStrength * 1.65;
    vec2 baseOffset = rayShift * ubuf.texelSize;

    vec3 redSample = sampleBackdrop(uv, baseOffset * (1.0 + DISPERSION), ubuf.blur);
    vec3 greenSample = sampleBackdrop(uv, baseOffset, ubuf.blur);
    vec3 blueSample = sampleBackdrop(uv, baseOffset * (1.0 - DISPERSION), ubuf.blur);
    vec3 transmitted = vec3(redSample.r, greenSample.g, blueSample.b);

    float viewCos = clamp(dot(surfaceNormal, vec3(0.0, 0.0, 1.0)), 0.0, 1.0);
    float f0 = pow((GLASS_IOR - 1.0) / (GLASS_IOR + 1.0), 2.0);
    float fresnel = f0 + (1.0 - f0) * pow(1.0 - viewCos, 5.0);
    fresnel *= bevel;

    float tintAmount = clamp(ubuf.glassTint.a * ubuf.opacityFactor, 0.0, 1.0);
    vec3 color = mix(transmitted, ubuf.glassTint.rgb, tintAmount);

    // Soft body reflection, a fine double rim and a restrained top reflection.
    vec2 lightDelta = (pixel - ubuf.lightPosition) /
                      max(1.0, min(ubuf.itemSize.x, ubuf.itemSize.y));
    float pointerSpecular = exp(-dot(lightDelta, lightDelta) * 62.0)
                          * ubuf.pointerIntensity;
    float topReflection = pow(1.0 - smoothstep(0.0, 0.52, uv.y), 3.0) * 0.075;
    float innerRim = exp(-pow((edgeDistance - 2.0) / 1.5, 2.0)) * 0.17;
    float outerRim = exp(-pow((edgeDistance - 7.0) / 3.0, 2.0)) * 0.055;

    color = mix(color, vec3(1.0), fresnel * 0.68);
    color += vec3(1.0) * (topReflection + innerRim + outerRim + pointerSpecular * 0.12);
    color = mix(color, ubuf.glassTint.rgb, bevel * 0.035);

    fragColor = vec4(color, inside * ubuf.qt_Opacity);
}
