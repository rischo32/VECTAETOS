// VORTEX — Scene Manager
// Clean separation: update() vs render()

import * as THREE from 'https://unpkg.com/three@0.160.0/build/three.module.js';
import { OrbitControls } from 'https://unpkg.com/three@0.160.0/examples/jsm/controls/OrbitControls.js';

export class SceneManager {

  constructor() {

    this.scene = null;
    this.camera = null;
    this.renderer = null;
    this.controls = null;

    this.time = 0;

    this.emPoint = null;
    this.gatePoints = [];
    this.targetPositions = [];

    this.splitting = false;
    this.splitProgress = 0;

    this.radius = 2.0;
  }

  // ----------------------------
  // INIT
  // ----------------------------
  init() {
    this.setupScene();
    this.setupCamera();
    this.setupRenderer();
    this.setupControls();
    this.setupLights();
    this.setupGrid();
    this.setupEMPoint();
  }

  setupScene() {
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x0b0d14);
  }

  setupCamera() {
    this.camera = new THREE.PerspectiveCamera(
      65,
      window.innerWidth / window.innerHeight,
      0.1,
      100
    );
    this.camera.position.set(0, 1.5, 3);
  }

  setupRenderer() {
    this.renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: false
    });

    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    document.body.appendChild(this.renderer.domElement);
  }

  setupControls() {
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.05;
    this.controls.enablePan = false;
  }

  setupLights() {
    const ambient = new THREE.AmbientLight(0xffffff, 0.4);
    this.scene.add(ambient);

    const dir = new THREE.DirectionalLight(0xffffff, 0.4);
    dir.position.set(2, 3, 2);
    this.scene.add(dir);
  }

  setupGrid() {
    const grid = new THREE.GridHelper(3, 30, 0x222222, 0x222222);
    grid.material.opacity = 0.08;
    grid.material.transparent = true;
    this.scene.add(grid);
  }

  setupEMPoint() {
    const geometry = new THREE.SphereGeometry(0.05, 32, 32);
    const material = new THREE.MeshStandardMaterial({
      color: 0x5DA9FF,
      emissive: 0x5DA9FF,
      emissiveIntensity: 0.8
    });

    this.emPoint = new THREE.Mesh(geometry, material);
    this.scene.add(this.emPoint);
  }

  // ----------------------------
  // SPLIT FROM DELTA
  // ----------------------------
  startSplit(W, H, D, intensity) {

    this.splitting = true;
    this.splitProgress = 0;

    this.targetPositions = [
      new THREE.Vector3(W * intensity * 1.5, 0, 0),
      new THREE.Vector3(0, H * intensity * 1.5, 0),
      new THREE.Vector3(0, 0, D * intensity * 1.5)
    ];

    this.gatePoints.forEach(p => this.scene.remove(p));
    this.gatePoints = [];

    const colors = [0x5DA9FF, 0xB76EFF, 0x6EFFA1];

    for (let i = 0; i < 3; i++) {
      const geo = new THREE.SphereGeometry(0.04, 24, 24);
      const mat = new THREE.MeshStandardMaterial({
        color: colors[i],
        emissive: colors[i],
        emissiveIntensity: 0.7
      });

      const mesh = new THREE.Mesh(geo, mat);
      this.scene.add(mesh);
      this.gatePoints.push(mesh);
    }

    if (this.emPoint) {
      this.scene.remove(this.emPoint);
      this.emPoint = null;
    }
  }

  // ----------------------------
  // UPDATE (LOGIC ONLY)
  // ----------------------------
  update() {

    this.time += 0.01;
    this.controls.update();

    if (!this.splitting && this.emPoint) {
      const scale = 1 + Math.sin(this.time * 4) * 0.05;
      this.emPoint.scale.set(scale, scale, scale);
    }

    if (this.splitting && this.splitProgress < 1) {

      this.splitProgress += 0.02;

      for (let i = 0; i < this.gatePoints.length; i++) {
        this.gatePoints[i].position.lerpVectors(
          new THREE.Vector3(0, 0, 0),
          this.targetPositions[i],
          this.splitProgress
        );
      }

    }
  }

  // ----------------------------
  // RENDER (DRAW ONLY)
  // ----------------------------
  render() {
    if (this.renderer && this.scene && this.camera) {
      this.renderer.render(this.scene, this.camera);
    }
  }

  // ----------------------------
  // RESIZE
  // ----------------------------
  onResize() {
    if (!this.camera || !this.renderer) return;

    this.camera.aspect = window.innerWidth / window.innerHeight;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(window.innerWidth, window.innerHeight);
  }

}
