'use client';

import React, { useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [responseMessage, setResponseMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    let video_url = e.target.VideoUrl.value;
    console.log(video_url);
    try {
      const response = await axios.post('http://localhost:8000/api/process-video/', {
        url: video_url
      });

      setResponseMessage(response.data.message);  // Display backend message
    } catch (error) {
      setResponseMessage('Error processing video. Make sure the link is correct!');
    }
  };


  return (
    <main className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-gray-800 text-white flex items-center justify-center px-4">
      <div className="max-w-2xl w-full text-center space-y-8">
        <h1 className="text-4xl md:text-5xl font-extrabold leading-tight">
          🚀 Clipify — Your AI-Powered Clip Curator
        </h1>
        <p className="text-lg md:text-xl text-gray-300">
          Paste a YouTube or video link, and we’ll auto-generate short, viral-worthy clips for TikTok, Reels, and more.
        </p>

        <form className="flex flex-col sm:flex-row items-center gap-4 mt-6" onSubmit={handleSubmit}>
          <input
            name='VideoUrl'
            type="url"
            placeholder="Enter YouTube/video link..."
            className="w-full p-3 rounded-lg text-grey-200 placeholder-gray-400 ring-2 ring-violet-500 focus:outline-none focus:ring-2 focus:ring-violet-500"
          />
          <button
            type="submit"
            className="px-10 py-3 rounded-lg font-semibold text-sm sm:text-base bg-violet-500 hover:bg-violet-600 focus:outline-2 focus:outline-offset-2 focus:outline-violet-500 active:bg-violet-700"
          >
            Clipify
          </button>
        </form>

        {responseMessage && <p>{responseMessage}</p>}
      </div>
    </main>
  );
}
