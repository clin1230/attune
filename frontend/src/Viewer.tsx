import { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

export default function Viewer({url,onSelect}:{url:string;onSelect:(id:string)=>void}) {
  const host=useRef<HTMLDivElement>(null);
  const callback=useRef(onSelect); callback.current=onSelect;
  const [error,setError]=useState('');
  useEffect(()=>{
    const element=host.current!;let disposed=false,frame=0;
    let renderer:THREE.WebGLRenderer;
    try{renderer=new THREE.WebGLRenderer({antialias:true,alpha:true});}
    catch {setError('3D is unavailable in this browser. Choose a rendered view.');return;}
    setError('');
    renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.toneMapping=THREE.ACESFilmicToneMapping;
    element.appendChild(renderer.domElement);
    const scene=new THREE.Scene();const camera=new THREE.PerspectiveCamera(38,1,.001,100);
    const pmrem=new THREE.PMREMGenerator(renderer),room=new RoomEnvironment();
    const env=pmrem.fromScene(room,.04);scene.environment=env.texture;room.dispose();pmrem.dispose();
    const controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;controls.minDistance=.15;controls.maxDistance=2;
    let model:THREE.Object3D|undefined;
    const disposeObject=(o:THREE.Object3D)=>o.traverse(n=>{if(n instanceof THREE.Mesh){n.geometry.dispose();const ms=Array.isArray(n.material)?n.material:[n.material];ms.forEach(m=>m.dispose());}});
    new GLTFLoader().load(url,g=>{
      if(disposed){disposeObject(g.scene);return;}
      model=g.scene;scene.add(model);
      const box=new THREE.Box3().setFromObject(model),center=box.getCenter(new THREE.Vector3()),size=box.getSize(new THREE.Vector3());
      const d=Math.max(size.x,size.y,size.z);camera.position.set(center.x+d*1.6,center.y+d*.8,center.z+d*2.2);controls.target.copy(center);controls.update();
    },undefined,()=>{if(!disposed)setError('No interactive model for this version yet. Choose a rendered view.');});
    const resize=()=>{const w=element.clientWidth,h=element.clientHeight;renderer.setSize(w,h);camera.aspect=w/Math.max(h,1);camera.updateProjectionMatrix();};
    const observer=new ResizeObserver(resize);observer.observe(element);resize();
    const ray=new THREE.Raycaster();let down=[0,0];
    const start=(e:PointerEvent)=>{down=[e.clientX,e.clientY]};
    const pick=(e:PointerEvent)=>{
      if(!model||Math.hypot(e.clientX-down[0],e.clientY-down[1])>5)return;
      const rect=renderer.domElement.getBoundingClientRect();ray.setFromCamera(new THREE.Vector2((e.clientX-rect.left)/rect.width*2-1,-(e.clientY-rect.top)/rect.height*2+1),camera);
      const hit=ray.intersectObject(model,true)[0];let o=hit?.object;
      while(o){if(o.userData.object_id){callback.current(o.userData.object_id);break;}o=o.parent!;}
    };
    renderer.domElement.addEventListener('pointerdown',start);renderer.domElement.addEventListener('pointerup',pick);
    const animate=()=>{frame=requestAnimationFrame(animate);controls.update();renderer.render(scene,camera)};animate();
    return()=>{disposed=true;cancelAnimationFrame(frame);observer.disconnect();controls.dispose();if(model)disposeObject(model);env.dispose();renderer.dispose();renderer.domElement.remove();};
  },[url]);
  return <div className="live-viewer" ref={host}>{error&&<div className="viewer-error">{error}</div>}</div>;
}
