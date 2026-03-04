// VORTEX — Scene Manager v2
// Cyclic split → hold → return

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

    this.state = "idle"; // idle | split | hold | return
    this.progress = 0;
    this.holdTime = 0;
  }

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
    this.renderer = new THREE.WebGLRenderer({ antialias: true });
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    document.body.appendChild(this.renderer.domElement);
  }

  setupControls() {
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.enablePan = false;
  }

  setupLights() {
    this.scene.add(new THREE.AmbientLight(0xffffff, 0.4));
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
    const geo = new THREE.SphereGeometry(0.05, 32, 32);
    const mat = new THREE.MeshStandardMaterial({
      color: 0x5DA9FF,
      emissive: 0x5DA9FF,
      emissiveIntensity: 0.8
    });
    this.emPoint = new THREE.Mesh(geo, mat);
    this.scene.add(this.emPoint);
  }

  startSplit(W, H, D, intensity) {

    this.state = "split";
    this.progress = 0;
    this.holdTime = 0;

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

  update() {

    this.time += 0.01;
    this.controls.update();

    if (this.state === "idle" && this.emPoint) {
      const scale = 1 + Math.sin(this.time * 4) * 0.05;
      this.emPoint.scale.set(scale, scale, scale);
    }

    if (this.state === "split") {

      this.progress += 0.02;

      for (let i = 0; i < this.gatePoints.length; i++) {
        this.gatePoints[i].position.lerpVectors(
          new THREE.Vector3(0, 0, 0),
          this.targetPositions[i],
          this.progress
        );
      }

      if (this.progress >= 1) {
        this.state = "hold";
      }
    }

    if (this.state === "hold") {
      this.holdTime += 1;

      if (this.holdTime > 60) { // cca 1 sekunda
        this.state = "return";
        this.progress = 1;
      }
    }

    if (this.state === "return") {

      this.progress -= 0.02;

      for (let i = 0; i < this.gatePoints.length; i++) {
        this.gatePoints[i].position.lerpVectors(
          new THREE.Vector3(0, 0, 0),
          this.targetPositions[i],
          this.progress
        );
      }

      if (this.progress <= 0) {

        this.gatePoints.forEach(p => this.scene.remove(p));
        this.gatePoints = [];

        this.setupEMPoint();

        this.state = "idle";
      }
    }
  }

  render() {
    this.renderer.render(this.scene, this.camera);
  }

  onResize() {
    this.camera.aspect = window.innerWidth / window.innerHeight;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(window.innerWidth, window.innerHeight);
  }
}
