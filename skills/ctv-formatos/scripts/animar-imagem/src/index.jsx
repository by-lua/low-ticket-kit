import React from 'react';
import {registerRoot,Composition,AbsoluteFill,Img,staticFile,useCurrentFrame,interpolate,getInputProps} from 'remotion';
// Formato "imagem animada" (4:5, 1080x1350): foto/arte base + camada de animação por código.
// Props (JSON): price, cta, band, arrow, arrowX, arrowY, sec, ring{left,top,width,height}, badgePos('bl'|'tr'), layout('pill'|'ring')
const P={price:'Desde $7.900',cta:'RECIBIR AHORA',band:'',arrow:true,arrowX:720,arrowY:1000,sec:7.2,badgePos:'bl',layout:'pill',ring:null,...getInputProps()};
const FPS=30, W=1080, H=1350, DUR=Math.round(P.sec*FPS);
const Arrow=({x,y})=>{const f=useCurrentFrame();const b=14*Math.abs(Math.sin(f/30*Math.PI*1.6));
  return <svg width="120" height="120" viewBox="0 0 100 100" style={{position:'absolute',left:x,top:y+b}}><path d="M38 6 H62 V50 H84 L50 92 L16 50 H38 Z" fill="#e8141c" stroke="#fff" strokeWidth="4" strokeLinejoin="round"/></svg>;};
const Hand=({tap})=><svg width="58" height="58" viewBox="0 0 64 64" style={{transform:`scale(${tap})`}}><circle cx="32" cy="32" r="30" fill="#fff" opacity=".25"/><path d="M22 10 L22 40 L29 34 L34 47 L40 45 L35 32 L45 32 Z" fill="#fff" stroke="#222" strokeWidth="2.5" strokeLinejoin="round"/></svg>;
const Ad=()=>{
  const f=useCurrentFrame();
  const zoom=interpolate(f,[0,DUR],[1,1.05]);
  const pulse=1+0.06*Math.sin(f/30*Math.PI*2*1.1);
  const ringA=0.5+0.5*Math.sin(f/30*Math.PI*2*1.1);
  const tap=1+0.14*Math.max(0,Math.sin(f/30*Math.PI*2*1.1));
  const badge=P.badgePos==='tr'?{top:16,right:16,transformOrigin:'100% 0%'}:{left:40,bottom:160,transformOrigin:'0% 100%'};
  return <AbsoluteFill style={{backgroundColor:'#000',overflow:'hidden'}}>
   <AbsoluteFill style={{transform:`scale(${zoom})`,transformOrigin:'50% 55%'}}>
     <Img src={staticFile('base.png')} style={{width:W,height:H}}/>
     {P.layout==='ring' && P.ring && <div style={{position:'absolute',...P.ring,borderRadius:70,border:'6px solid #fff',opacity:0.35+0.55*ringA,transform:`scale(${1+0.05*ringA})`,boxShadow:'0 0 28px 6px rgba(255,214,0,.55)'}}/>}
     {P.layout==='ring' && P.arrow && <Arrow x={P.arrowX} y={P.arrowY}/>}
   </AbsoluteFill>
   {P.band && <div style={{position:'absolute',top:42,left:56,right:56,background:'#ffd60a',color:'#111',fontFamily:'Arial',fontWeight:800,fontSize:58,textAlign:'center',padding:'20px 24px',borderRadius:26,border:'3px solid #111',boxShadow:'0 4px 14px rgba(0,0,0,.35)'}}>{P.band}</div>}
   {P.price && <div style={{position:'absolute',...badge,background:'#17a84b',color:'#fff',fontFamily:'Arial',fontWeight:800,fontSize:P.badgePos==='tr'?40:56,padding:P.badgePos==='tr'?'10px 28px':'14px 42px',borderRadius:60,boxShadow:'0 4px 14px rgba(0,0,0,.4)',transform:`scale(${pulse})`}}>{P.price}</div>}
   {P.layout==='pill' && P.arrow && <Arrow x={P.arrowX} y={P.arrowY}/>}
   {P.layout==='pill' && P.cta && <div style={{position:'absolute',left:110,bottom:42,width:860,height:104,borderRadius:56,background:'#d8121c',border:'5px solid #fff',boxShadow:'0 6px 18px rgba(0,0,0,.45)',display:'flex',alignItems:'center',justifyContent:'space-between',padding:'0 38px 0 52px',boxSizing:'border-box',transform:`scale(${pulse})`,transformOrigin:'50% 100%'}}>
     <span style={{color:'#fff',fontFamily:'Arial',fontWeight:800,fontSize:50,letterSpacing:1}}>{P.cta}</span><Hand tap={tap}/></div>}
  </AbsoluteFill>;};
const Root=()=> <Composition id="Anim" component={Ad} width={W} height={H} fps={FPS} durationInFrames={DUR}/>;
registerRoot(Root);
