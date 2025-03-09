"use client";

import Tilt from "react-parallax-tilt";
import { useState, useEffect } from "react";

export default function Home() {
  const [bgColor, setBgColor] = useState("rgb(0, 100, 0)"); // Initial color (green)
  const [tiltX, setTiltX] = useState(0); // Initial tilt value

  const handleTiltChange = (event) => {
    const { tiltX, tiltY } = event; // Use tiltX and tiltY from the event object
    const red = Math.min(255, Math.abs(tiltX) * 5);
    const blue = Math.min(255, Math.abs(tiltY) * 5);
    setBgColor(`rgb(${red}, 100, ${blue})`);
  };

  const handleKeyDown = (event) => {
    if (event.key === "ArrowLeft") {
      setTiltX(-10); // Tilt left
    } else if (event.key === "ArrowRight") {
      setTiltX(10); // Tilt right
    }
  };

  const handleKeyUp = (event) => {
    if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
      setTiltX(0); // Reset tilt when key is released
    }
  };

  useEffect(() => {
    // Add event listeners for keydown and keyup
    window.addEventListener("keydown", handleKeyDown);
    window.addEventListener("keyup", handleKeyUp);

    // Cleanup the event listeners on component unmount
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      window.removeEventListener("keyup", handleKeyUp);
    };
  }, []);

  return (
    <div className="flex flex-col justify-center items-center h-screen space-y-6">
      <Tilt
        tiltX={tiltX} // Set the tiltX value based on the state
        onMove={(e) => handleTiltChange(e)}
        glareEnable={true}
        glareMaxOpacity={0.3}
        glareColor="#ffffff"
        glarePosition="all"
      >
        <div
          className="w-80 h-80 rounded-3xl flex justify-center items-center transition-all duration-200"
          style={{ backgroundColor: bgColor }}
        >
          <img src="/file.svg" alt="React Logo" className="w-32 h-32" />
          <h1> Hello Tilt </h1>
        </div>
      </Tilt>
    </div>
  );
}
