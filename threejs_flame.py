"""Self-contained Three.js WebGL 3D combustion morphology renderer."""

from __future__ import annotations

import math
from typing import Any


def _finite_or_default(value: Any, default: float, min_v: float | None = None, max_v: float | None = None) -> float:
    """Coerce numeric telemetry safely with finite and optional bound guards."""
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(parsed):
        return default
    if min_v is not None:
        parsed = max(min_v, parsed)
    if max_v is not None:
        parsed = min(max_v, parsed)
    return parsed


def generate_threejs_flame_html(
    gravity_g: float = 0.0,
    airflow_cm_s: float = 10.0,
    oxygen_pct: float = 21.0,
    pressure_kpa: float = 101.3,
    peak_temp_k: float = 1380.0,
    is_extinguished: bool = False,
    **kwargs: Any,
) -> str:
    """Return standalone HTML/Three.js WebGL visualization for combustion morphology."""
    del kwargs  # Preserve compatibility with optional caller metadata.
    g_val = _finite_or_default(gravity_g, 0.0, 0.0, 3.0)
    v_val = _finite_or_default(airflow_cm_s, 10.0, 0.0, 200.0)
    o2_val = _finite_or_default(oxygen_pct, 21.0, 0.0, 100.0)
    p_val = _finite_or_default(pressure_kpa, 101.3, 1.0, 500.0)
    temp_k = _finite_or_default(peak_temp_k, 1380.0, 250.0, 3500.0)

    is_zero_g_js = "true" if g_val <= 0.08 else "false"
    is_ext_js = "true" if bool(is_extinguished) else "false"
    status_label = "EXTINGUISHED" if bool(is_extinguished) else ("0g SPHERICAL" if g_val <= 0.08 else "BUOYANT PLUME")
    hud_telemetry = f"g={g_val:.2f}g | V={v_val:.0f}cm/s | O2={o2_val:.1f}% | P={p_val:.1f}kPa | T_peak={temp_k:.0f}K"

    template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<style>
  html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #050811;
    color: #e2e8f0;
    font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif;
  }
  #canvas-container {
    width: 100%;
    height: 100%;
    min-height: 430px;
    position: relative;
  }
  .hud-overlay {
    position: absolute;
    top: 12px;
    left: 12px;
    z-index: 10;
    background: rgba(15, 23, 42, 0.82);
    border: 1px solid rgba(56, 189, 248, 0.35);
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 12px;
    line-height: 1.45;
    pointer-events: none;
  }
  .hud-title {
    font-weight: 700;
    color: #38bdf8;
    letter-spacing: 0.04em;
  }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>
<div id="canvas-container">
  <div class="hud-overlay">
    <div class="hud-title">3D COMBUSTION MORPHOLOGY (__STATUS_LABEL__)</div>
    <div>__HUD_TELEMETRY__</div>
  </div>
</div>
<script>
(function() {
  const container = document.getElementById("canvas-container");
  const is0g = __IS_0G__;
  const isExt = __IS_EXT__;
  const gVal = __G_VAL__;
  const vVal = __V_VAL__;
  const o2Val = __O2_VAL__;
  const pVal = __P_VAL__;
  const particleCount = 450;

  if (typeof THREE === "undefined") {
    const fallback = document.createElement("div");
    fallback.style.cssText = "padding:80px 20px;text-align:center;color:#94a3b8;font-size:13px;";
    fallback.textContent = "WebGL Three.js viewport initialized offline (" + "__HUD_TELEMETRY__" + ")";
    container.appendChild(fallback);
    return;
  }

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x050811);

  const width = container.clientWidth || window.innerWidth || 720;
  const height = container.clientHeight || 440;
  const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
  camera.position.set(3.2, 2.1, 4.0);

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  container.appendChild(renderer.domElement);

  let controls = null;
  if (typeof THREE.OrbitControls === "function") {
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.autoRotate = true;
    controls.autoRotateSpeed = is0g ? 0.65 : 1.15;
  }

  const gridHelper = new THREE.GridHelper(6, 12, 0x1e293b, 0x0f172a);
  gridHelper.position.y = -1.2;
  scene.add(gridHelper);

  const ambientLight = new THREE.AmbientLight(0x94a3b8, 0.8);
  scene.add(ambientLight);
  const pointLight = new THREE.PointLight(isExt ? 0x64748b : (o2Val > 30 ? 0x38bdf8 : 0xf97316), 2.0, 20);
  pointLight.position.set(0, 0.4, 0);
  scene.add(pointLight);

  const fuelGeom = new THREE.SphereGeometry(0.24, 24, 24);
  const fuelMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.6 });
  const fuelSample = new THREE.Mesh(fuelGeom, fuelMat);
  scene.add(fuelSample);

  const elongation = is0g ? 1.0 : Math.min(3.4, 1.15 + gVal * 1.9);
  const driftX = Math.min(1.8, vVal * 0.025);
  const flameRadius = isExt ? 0.42 : Math.max(0.45, Math.min(1.4, (o2Val / 21.0) * (101.3 / Math.max(20.0, pVal)) * 0.65));

  const coreGeom = new THREE.SphereGeometry(flameRadius, 32, 32);
  const coreColor = isExt ? 0x475569 : (o2Val >= 30.0 ? 0x38bdf8 : 0xf97316);
  const coreMat = new THREE.MeshBasicMaterial({
    color: coreColor,
    transparent: true,
    opacity: isExt ? 0.22 : 0.48,
    wireframe: false
  });
  const flameCore = new THREE.Mesh(coreGeom, coreMat);
  flameCore.scale.set(is0g ? 1.0 : 1.0 + driftX * 0.25, elongation, 1.0);
  flameCore.position.x = driftX * 0.35;
  scene.add(flameCore);

  const positions = new Float32Array(particleCount * 3);
  const velocities = new Float32Array(particleCount * 3);
  for (let i = 0; i < particleCount; i++) {
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);
    const r = 0.25 + Math.random() * flameRadius;
    positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
    positions[i * 3 + 1] = r * Math.cos(phi) * elongation;
    positions[i * 3 + 2] = r * Math.sin(phi) * Math.sin(theta);

    velocities[i * 3] = 0.002 + vVal * 0.0004;
    velocities[i * 3 + 1] = is0g ? (Math.random() - 0.5) * 0.004 : (0.006 + gVal * 0.025);
    velocities[i * 3 + 2] = (Math.random() - 0.5) * 0.004;
  }

  const partGeom = new THREE.BufferGeometry();
  partGeom.setAttribute("position", new THREE.BufferAttribute(positions, 3));
  const partMat = new THREE.PointsMaterial({
    color: isExt ? 0x64748b : (is0g ? 0x60a5fa : 0xfbbf24),
    size: 0.055,
    transparent: true,
    opacity: isExt ? 0.35 : 0.85
  });
  const flameParticles = new THREE.Points(partGeom, partMat);
  scene.add(flameParticles);

  function animate() {
    requestAnimationFrame(animate);
    const pos = partGeom.attributes.position.array;
    for (let i = 0; i < particleCount; i++) {
      const idx = i * 3;
      pos[idx] += velocities[idx];
      pos[idx + 1] += velocities[idx + 1];
      pos[idx + 2] += velocities[idx + 2];
      const dist = Math.sqrt(pos[idx] * pos[idx] + pos[idx + 1] * pos[idx + 1] + pos[idx + 2] * pos[idx + 2]);
      if (dist > flameRadius * (is0g ? 1.45 : 2.3)) {
        const angle = Math.random() * Math.PI * 2;
        pos[idx] = Math.cos(angle) * 0.2;
        pos[idx + 1] = is0g ? (Math.random() - 0.5) * 0.25 : -0.15;
        pos[idx + 2] = Math.sin(angle) * 0.2;
      }
    }
    partGeom.attributes.position.needsUpdate = true;
    if (controls) {
      controls.update();
    }
    renderer.render(scene, camera);
  }
  animate();

  window.addEventListener("resize", function() {
    const w = container.clientWidth || window.innerWidth || 720;
    const h = container.clientHeight || 440;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h);
  });
})();
</script>
</body>
</html>
"""
    return (
        template.replace("__STATUS_LABEL__", status_label)
        .replace("__HUD_TELEMETRY__", hud_telemetry)
        .replace("__IS_0G__", is_zero_g_js)
        .replace("__IS_EXT__", is_ext_js)
        .replace("__G_VAL__", f"{g_val:.4f}")
        .replace("__V_VAL__", f"{v_val:.2f}")
        .replace("__O2_VAL__", f"{o2_val:.2f}")
        .replace("__P_VAL__", f"{p_val:.2f}")
    )
