/**
 * Hero accueil — scène 3D WebGL (fil de fer + particules + lueur).
 */
(function () {
  const canvas = document.getElementById("home-hero-canvas");
  const hero = document.querySelector(".xd-hero") || document.querySelector(".home-hero");
  if (!canvas || !hero) return;

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const isMobile = window.matchMedia("(max-width: 900px), (pointer: coarse)").matches;
  if (reduceMotion) return;

  const gl = canvas.getContext("webgl", { alpha: true, antialias: true, powerPreference: "low-power" });
  if (!gl) return;

  const COLORS = {
    green: [0.08, 0.18, 0.12],
    greenLight: [0.28, 0.55, 0.38],
    gold: [0.85, 0.65, 0.28],
    goldBright: [1.0, 0.85, 0.5],
    terra: [0.85, 0.38, 0.28],
    cream: [1.0, 0.98, 0.94],
  };

  function compile(type, src) {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, src);
    gl.compileShader(shader);
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
      console.warn("home-hero-3d:", gl.getShaderInfoLog(shader));
      return null;
    }
    return shader;
  }

  function linkProgram(vsSrc, fsSrc) {
    const vs = compile(gl.VERTEX_SHADER, vsSrc);
    const fs = compile(gl.FRAGMENT_SHADER, fsSrc);
    if (!vs || !fs) return null;
    const prog = gl.createProgram();
    gl.attachShader(prog, vs);
    gl.attachShader(prog, fs);
    gl.linkProgram(prog);
    return gl.getProgramParameter(prog, gl.LINK_STATUS) ? prog : null;
  }

  const lineVert = `
    attribute vec3 a_pos;
    attribute vec3 a_color;
    attribute float a_alpha;
    uniform mat4 u_mvp;
    varying vec3 v_color;
    varying float v_alpha;
    void main() {
      v_color = a_color;
      v_alpha = a_alpha;
      gl_Position = u_mvp * vec4(a_pos, 1.0);
    }
  `;
  const lineFrag = `
    precision mediump float;
    varying vec3 v_color;
    varying float v_alpha;
    void main() {
      gl_FragColor = vec4(v_color, v_alpha);
    }
  `;

  const pointVert = `
    attribute vec3 a_pos;
    attribute float a_size;
    attribute vec3 a_color;
    attribute float a_alpha;
    uniform mat4 u_view;
    uniform mat4 u_proj;
    varying vec3 v_color;
    varying float v_alpha;
    void main() {
      v_color = a_color;
      v_alpha = a_alpha;
      vec4 view = u_view * vec4(a_pos, 1.0);
      gl_Position = u_proj * view;
      gl_PointSize = a_size * (340.0 / max(-view.z, 0.35));
    }
  `;
  const pointFrag = `
    precision mediump float;
    varying vec3 v_color;
    varying float v_alpha;
    void main() {
      vec2 uv = gl_PointCoord - 0.5;
      float d = length(uv);
      if (d > 0.5) discard;
      float core = smoothstep(0.5, 0.0, d);
      float halo = smoothstep(0.5, 0.12, d);
      gl_FragColor = vec4(v_color, v_alpha * mix(halo, core, 0.65));
    }
  `;

  const lineProgram = linkProgram(lineVert, lineFrag);
  const pointProgram = linkProgram(pointVert, pointFrag);
  if (!lineProgram || !pointProgram) return;

  const lineU = {
    mvp: gl.getUniformLocation(lineProgram, "u_mvp"),
    pos: gl.getAttribLocation(lineProgram, "a_pos"),
    color: gl.getAttribLocation(lineProgram, "a_color"),
    alpha: gl.getAttribLocation(lineProgram, "a_alpha"),
  };
  const pointU = {
    view: gl.getUniformLocation(pointProgram, "u_view"),
    proj: gl.getUniformLocation(pointProgram, "u_proj"),
    pos: gl.getAttribLocation(pointProgram, "a_pos"),
    size: gl.getAttribLocation(pointProgram, "a_size"),
    color: gl.getAttribLocation(pointProgram, "a_color"),
    alpha: gl.getAttribLocation(pointProgram, "a_alpha"),
  };

  function buildOctahedronLines(size) {
    const v = [
      [size, 0, 0],
      [-size, 0, 0],
      [0, size, 0],
      [0, -size, 0],
      [0, 0, size],
      [0, 0, -size],
    ];
    const edges = [
      [0, 2], [0, 3], [0, 4], [0, 5],
      [1, 2], [1, 3], [1, 4], [1, 5],
      [2, 4], [2, 5], [3, 4], [3, 5],
    ];
    const out = [];
    for (const [a, b] of edges) {
      out.push(...v[a], ...v[b]);
    }
    return out;
  }

  function buildRingLines(radius, segments) {
    const out = [];
    for (let i = 0; i < segments; i++) {
      const a1 = (i / segments) * Math.PI * 2;
      const a2 = ((i + 1) / segments) * Math.PI * 2;
      out.push(
        Math.cos(a1) * radius, 0, Math.sin(a1) * radius,
        Math.cos(a2) * radius, 0, Math.sin(a2) * radius
      );
    }
    return out;
  }

  function buildHelixLines(turns, points, radius, height) {
    const out = [];
    for (let i = 0; i < points - 1; i++) {
      const t1 = i / (points - 1);
      const t2 = (i + 1) / (points - 1);
      const a1 = t1 * turns * Math.PI * 2;
      const a2 = t2 * turns * Math.PI * 2;
      out.push(
        Math.cos(a1) * radius, (t1 - 0.5) * height, Math.sin(a1) * radius,
        Math.cos(a2) * radius, (t2 - 0.5) * height, Math.sin(a2) * radius
      );
    }
    return out;
  }

  const wireMeshes = isMobile
    ? [
        { lines: buildRingLines(1.5, 48), color: COLORS.gold, alpha: 0.42, pos: [1.6, 0.15, -2.8], scale: 1, spin: [0.12, 0.28, 0.08] },
        { lines: buildOctahedronLines(0.95), color: COLORS.greenLight, alpha: 0.38, pos: [-1.4, -0.1, -3.2], scale: 1, spin: [-0.1, 0.22, 0.14] },
      ]
    : [
        { lines: buildRingLines(2.4, 80), color: COLORS.gold, alpha: 0.55, pos: [2.6, 0.3, -2.4], scale: 1, spin: [0.1, 0.32, 0.06] },
        { lines: buildRingLines(1.5, 64), color: COLORS.terra, alpha: 0.42, pos: [-0.2, 0.6, -1.6], scale: 1, spin: [0.22, -0.18, 0.3], tilt: 1.1 },
        { lines: buildOctahedronLines(1.25), color: COLORS.greenLight, alpha: 0.5, pos: [-2.3, -0.1, -3.2], scale: 1, spin: [-0.08, 0.24, 0.12] },
        { lines: buildHelixLines(2.5, 48, 1.15, 2.6), color: COLORS.goldBright, alpha: 0.38, pos: [0.9, 0, -3.6], scale: 1, spin: [0.05, 0.4, 0.02] },
        { lines: buildRingLines(0.85, 40), color: COLORS.cream, alpha: 0.28, pos: [1.2, -0.4, -2.0], scale: 1, spin: [0.35, 0.15, -0.2], tilt: 0.3 },
      ];

  const wireBuffers = wireMeshes.map((mesh) => {
    const positions = new Float32Array(mesh.lines);
    const colors = new Float32Array((positions.length / 3) * 3);
    const alphas = new Float32Array(positions.length / 3);
    for (let i = 0; i < positions.length / 3; i++) {
      colors[i * 3] = mesh.color[0];
      colors[i * 3 + 1] = mesh.color[1];
      colors[i * 3 + 2] = mesh.color[2];
      alphas[i] = mesh.alpha;
    }
    const bufPos = gl.createBuffer();
    const bufCol = gl.createBuffer();
    const bufAlp = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, bufPos);
    gl.bufferData(gl.ARRAY_BUFFER, positions, gl.STATIC_DRAW);
    gl.bindBuffer(gl.ARRAY_BUFFER, bufCol);
    gl.bufferData(gl.ARRAY_BUFFER, colors, gl.STATIC_DRAW);
    gl.bindBuffer(gl.ARRAY_BUFFER, bufAlp);
    gl.bufferData(gl.ARRAY_BUFFER, alphas, gl.STATIC_DRAW);
    return { vertexCount: positions.length / 3, bufPos, bufCol, bufAlp, mesh };
  });

  const particleCount = isMobile ? 120 : 280;
  const positions = [];
  const sizes = [];
  const colors = [];
  const alphas = [];
  const glow = [];
  const seeds = [];

  function pushParticle(x, y, z, size, color, alpha, isGlow) {
    positions.push(x, y, z);
    sizes.push(size);
    colors.push(color[0], color[1], color[2]);
    alphas.push(alpha);
    glow.push(isGlow ? 1 : 0);
    seeds.push(Math.random() * Math.PI * 2, Math.random() * 0.9 + 0.15, Math.random() * 0.7 + 0.35);
  }

  const layers = [
    { radius: 3.2, spread: 0.6, y: 0.1, color: COLORS.green, size: 4.5 },
    { radius: 2.6, spread: 0.4, y: 0.35, color: COLORS.gold, size: 5.8 },
    { radius: 3.8, spread: 0.7, y: -0.2, color: COLORS.greenLight, size: 3.8 },
    { radius: 2.0, spread: 0.3, y: 0.5, color: COLORS.terra, size: 6.2 },
  ];

  for (let i = 0; i < particleCount; i++) {
    const layer = layers[i % layers.length];
    const t = (i / particleCount) * Math.PI * 2 * 1.7;
    const r = layer.radius + (Math.random() - 0.5) * layer.spread;
    pushParticle(
      Math.cos(t + i * 0.4) * r,
      layer.y + (Math.random() - 0.5) * 1.6,
      Math.sin(t * 0.85 + i * 0.25) * r - 4.8,
      layer.size * (0.65 + Math.random() * 0.7),
      layer.color,
      0.28 + Math.random() * 0.38,
      false
    );
  }

  const glowCount = isMobile ? 18 : 36;
  for (let i = 0; i < glowCount; i++) {
    const ang = (i / glowCount) * Math.PI * 2;
    const r = 1.4 + Math.random() * 2.2;
    pushParticle(
      Math.cos(ang) * r,
      (Math.random() - 0.5) * 1.2,
      Math.sin(ang) * r - 3.0,
      16 + Math.random() * 14,
      i % 3 === 0 ? COLORS.goldBright : i % 3 === 1 ? COLORS.cream : COLORS.terra,
      0.5 + Math.random() * 0.35,
      true
    );
  }

  const posBuf = gl.createBuffer();
  const sizeBuf = gl.createBuffer();
  const colorBuf = gl.createBuffer();
  const alphaBuf = gl.createBuffer();
  const animatedPos = new Float32Array(positions);

  function bindArray(buf, loc, data, size, dynamic) {
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, data, dynamic ? gl.DYNAMIC_DRAW : gl.STATIC_DRAW);
    gl.enableVertexAttribArray(loc);
    gl.vertexAttribPointer(loc, size, gl.FLOAT, false, 0, 0);
  }

  bindArray(posBuf, pointU.pos, new Float32Array(positions), 3, true);
  bindArray(sizeBuf, pointU.size, new Float32Array(sizes), 1, false);
  bindArray(colorBuf, pointU.color, new Float32Array(colors), 3, false);
  bindArray(alphaBuf, pointU.alpha, new Float32Array(alphas), 1, false);

  const total = positions.length / 3;
  const normalCount = total - glowCount;

  gl.enable(gl.BLEND);
  gl.enable(gl.DEPTH_TEST);
  gl.depthFunc(gl.LEQUAL);

  let width = 0;
  let height = 0;
  let mouseX = 0;
  let mouseY = 0;
  let targetMouseX = 0;
  let targetMouseY = 0;
  let rafId = 0;

  function resize() {
    const rect = hero.getBoundingClientRect();
    const dpr = Math.min(window.devicePixelRatio || 1, isMobile ? 1.5 : 2);
    width = Math.max(1, Math.floor(rect.width * dpr));
    height = Math.max(1, Math.floor(rect.height * dpr));
    canvas.width = width;
    canvas.height = height;
    canvas.style.width = rect.width + "px";
    canvas.style.height = rect.height + "px";
    gl.viewport(0, 0, width, height);
  }

  function perspective(fov, aspect, near, far) {
    const f = 1.0 / Math.tan(fov / 2);
    const nf = 1 / (near - far);
    return new Float32Array([
      f / aspect, 0, 0, 0,
      0, f, 0, 0,
      0, 0, (far + near) * nf, -1,
      0, 0, 2 * far * near * nf, 0,
    ]);
  }

  function multiply(a, b) {
    const out = new Float32Array(16);
    for (let i = 0; i < 4; i++) {
      for (let j = 0; j < 4; j++) {
        out[i * 4 + j] =
          a[i * 4 + 0] * b[0 * 4 + j] +
          a[i * 4 + 1] * b[1 * 4 + j] +
          a[i * 4 + 2] * b[2 * 4 + j] +
          a[i * 4 + 3] * b[3 * 4 + j];
      }
    }
    return out;
  }

  function rotationY(a) {
    const c = Math.cos(a);
    const s = Math.sin(a);
    return new Float32Array([c, 0, s, 0, 0, 1, 0, 0, -s, 0, c, 0, 0, 0, 0, 1]);
  }

  function rotationX(a) {
    const c = Math.cos(a);
    const s = Math.sin(a);
    return new Float32Array([1, 0, 0, 0, 0, c, -s, 0, 0, s, c, 0, 0, 0, 0, 1]);
  }

  function rotationZ(a) {
    const c = Math.cos(a);
    const s = Math.sin(a);
    return new Float32Array([c, -s, 0, 0, s, c, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]);
  }

  function translation(x, y, z) {
    return new Float32Array([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, x, y, z, 1]);
  }

  function scale(s) {
    return new Float32Array([s, 0, 0, 0, 0, s, 0, 0, 0, 0, s, 0, 0, 0, 0, 1]);
  }

  function bindLineAttribs(buf) {
    gl.bindBuffer(gl.ARRAY_BUFFER, buf.bufPos);
    gl.enableVertexAttribArray(lineU.pos);
    gl.vertexAttribPointer(lineU.pos, 3, gl.FLOAT, false, 0, 0);
    gl.bindBuffer(gl.ARRAY_BUFFER, buf.bufCol);
    gl.enableVertexAttribArray(lineU.color);
    gl.vertexAttribPointer(lineU.color, 3, gl.FLOAT, false, 0, 0);
    gl.bindBuffer(gl.ARRAY_BUFFER, buf.bufAlp);
    gl.enableVertexAttribArray(lineU.alpha);
    gl.vertexAttribPointer(lineU.alpha, 1, gl.FLOAT, false, 0, 0);
  }

  function drawWireMeshes(proj, view, t) {
    gl.useProgram(lineProgram);
    for (const wb of wireBuffers) {
      const m = wb.mesh;
      const spin = m.spin || [0.1, 0.2, 0.05];
      const local =
        multiply(
          translation(m.pos[0], m.pos[1], m.pos[2]),
          multiply(
            rotationY(t * spin[1] + mouseX * 0.2),
            multiply(
              rotationX((m.tilt || 0.55) + t * spin[0] + mouseY * 0.15),
              multiply(rotationZ(t * spin[2]), scale(m.scale || 1))
            )
          )
        );
      const mvp = multiply(proj, multiply(view, local));
      gl.uniformMatrix4fv(lineU.mvp, false, mvp);
      bindLineAttribs(wb);
      gl.drawArrays(gl.LINES, 0, wb.vertexCount);
    }
  }

  function animateParticles(t) {
    for (let i = 0; i < total; i++) {
      const base = (i * 3) % seeds.length;
      const seed = seeds[base];
      const amp = seeds[base + 1];
      const speed = seeds[base + 2];
      const ix = i * 3;
      const drift = glow[i] ? 0.12 : 0.07;
      animatedPos[ix] = positions[ix] + Math.sin(t * 2.4 * speed + seed) * amp * drift;
      animatedPos[ix + 1] = positions[ix + 1] + Math.cos(t * 1.9 * speed + seed) * amp * drift * 0.85;
      animatedPos[ix + 2] = positions[ix + 2] + Math.sin(t * 1.4 * speed + seed * 1.5) * amp * drift * 0.7;
    }
    gl.bindBuffer(gl.ARRAY_BUFFER, posBuf);
    gl.bufferSubData(gl.ARRAY_BUFFER, 0, animatedPos);
  }

  function drawPoints(proj, view, additive) {
    gl.useProgram(pointProgram);
    gl.uniformMatrix4fv(pointU.proj, false, proj);
    gl.uniformMatrix4fv(pointU.view, false, view);
    gl.bindBuffer(gl.ARRAY_BUFFER, posBuf);
    gl.enableVertexAttribArray(pointU.pos);
    gl.vertexAttribPointer(pointU.pos, 3, gl.FLOAT, false, 0, 0);
    gl.bindBuffer(gl.ARRAY_BUFFER, sizeBuf);
    gl.enableVertexAttribArray(pointU.size);
    gl.vertexAttribPointer(pointU.size, 1, gl.FLOAT, false, 0, 0);
    gl.bindBuffer(gl.ARRAY_BUFFER, colorBuf);
    gl.enableVertexAttribArray(pointU.color);
    gl.vertexAttribPointer(pointU.color, 3, gl.FLOAT, false, 0, 0);
    gl.bindBuffer(gl.ARRAY_BUFFER, alphaBuf);
    gl.enableVertexAttribArray(pointU.alpha);
    gl.vertexAttribPointer(pointU.alpha, 1, gl.FLOAT, false, 0, 0);

    if (additive) {
      gl.blendFunc(gl.SRC_ALPHA, gl.ONE);
      gl.drawArrays(gl.POINTS, normalCount, glowCount);
      gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
    } else {
      gl.drawArrays(gl.POINTS, 0, normalCount);
    }
  }

  function draw(time) {
    const t = time * 0.00032;
    mouseX += (targetMouseX - mouseX) * 0.055;
    mouseY += (targetMouseY - mouseY) * 0.055;

    gl.clearColor(0, 0, 0, 0);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    const aspect = width / height;
    const proj = perspective(Math.PI / 4, aspect, 0.1, 48);
    const sway = Math.sin(t * 0.6) * 0.08;
    const rotY = rotationY(t * 0.75 + mouseX * 0.42 + sway);
    const rotX = rotationX(0.22 + mouseY * 0.28);
    const trans = translation(isMobile ? 0.2 : 0.5, 0.05, -6.4);
    const view = multiply(multiply(trans, rotX), rotY);

    drawWireMeshes(proj, view, t);
    animateParticles(t);
    drawPoints(proj, view, false);
    drawPoints(proj, view, true);

    rafId = requestAnimationFrame(draw);
  }

  hero.addEventListener("mousemove", (e) => {
    const rect = hero.getBoundingClientRect();
    targetMouseX = ((e.clientX - rect.left) / rect.width - 0.5) * 2;
    targetMouseY = ((e.clientY - rect.top) / rect.height - 0.5) * 2;
  });

  if (!isMobile) {
    hero.addEventListener("mouseleave", () => {
      targetMouseX = 0;
      targetMouseY = 0;
    });
  }

  const ro = typeof ResizeObserver !== "undefined" ? new ResizeObserver(resize) : null;
  if (ro) ro.observe(hero);
  else window.addEventListener("resize", resize);
  resize();
  rafId = requestAnimationFrame(draw);

  document.addEventListener("visibilitychange", () => {
    if (document.hidden) cancelAnimationFrame(rafId);
    else rafId = requestAnimationFrame(draw);
  });
})();
