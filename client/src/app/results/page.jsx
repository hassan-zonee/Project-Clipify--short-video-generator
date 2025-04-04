import Clip from "@/components/Clip";
import { ArrowLeftIcon } from "@heroicons/react/solid"; // Import Heroicon for back button
import React from "react";
import Link from 'next/link';

const ResultsPage = () => {

  // Sample data to simulate the results
  const clips = [
    {
      title: "Clip 1: Funny Moments",
      thumbnail: "https://picsum.photos/400/225?random=1", // Random image from Lorem Picsum
      url: "#", // Replace with actual video link
    },
    {
      title: "Clip 2: Best Reactions",
      thumbnail: "https://picsum.photos/400/225?random=2", // Random image from Lorem Picsum
      url: "#", // Replace with actual video link
    },
    {
      title: "Clip 3: Epic Fail",
      thumbnail: "https://picsum.photos/400/225?random=3", // Random image from Lorem Picsum
      url: "#", // Replace with actual video link
    },
    // Add more clips if needed
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-gray-800 text-white flex items-center justify-center px-4 py-20">
      <div className="max-w-2xl w-full text-center space-y-8">
        {/* Back Button */}
        <button
          className="absolute top-4 left-4 p-2 bg-violet-500 focus:outline-none focus:bg-violet-400 rounded-full text-white transition-all cursor-pointer"
        >
            <Link href="/">
                <ArrowLeftIcon className="w-6 h-6" />
            </Link>
        </button>

        <h1 className="text-4xl md:text-4xl font-extrabold leading-tight">
          Your Generated Clips
        </h1>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 py-10">
          {clips.map((clip, index) => (
            <Clip key={index} title={clip.title} thumbnail={clip.thumbnail} url={clip.url} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;
