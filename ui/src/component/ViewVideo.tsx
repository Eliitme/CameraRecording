"use client";

import React from "react";
import dynamic from "next/dynamic";

const ReactPlayer = dynamic(() => import("react-player"), { ssr: false });

const ViewVideo = ({ videoKey }: { videoKey: string }) => {
  return (
    <ReactPlayer
      url={`http://flask_app:8080/recordings/${videoKey}`}
      controls={true}
      width={"100%"}
      height={"100%"}
    />
  );
};

export default ViewVideo;
