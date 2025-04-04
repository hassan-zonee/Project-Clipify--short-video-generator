// app/components/Clip.tsx
import React from 'react';
import { DownloadIcon, PlayIcon } from '@heroicons/react/solid';

const Clip = ({ title, thumbnail, url }) => {
  return (
    <div className="bg-white rounded-lg shadow-xl overflow-hidden hover:scale-105 transition-all duration-300 ease-in-out transform hover:shadow-2xl relative">
        <div className="relative w-full pb-[177.78%]"> {/* 9:16 Aspect Ratio */}
            <img
            src={thumbnail}
            alt={title}
            className="absolute inset-0 w-full h-full object-cover rounded-t-lg"
            />
        </div>

        <div className="absolute inset-0 flex items-center justify-center">
            <button className="bg-violet-500 p-3 rounded-full shadow-lg hover:bg-gray-200 transition duration-200 ease-in-out cursor-pointer focus:outline-none focus:bg-violet-400">
                <PlayIcon className="w-8 h-8 text-white " />
            </button>
        </div>


        <button
            className="cursor-pointer absolute w-full bottom-0 transform -translate-x-1/2 bg-violet-500 text-white py-3 px-8 text-center text-lg font-medium transition-colors duration-300 ease-in-out focus:outline-none focus:bg-violet-400"
        >
            <div className="flex flex-row items-center justify-between">
                <span>Download</span>
                <DownloadIcon className="w-5 h-5" />
            </div>
        </button>

    </div>
  );
};

export default Clip;
