import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

function DiagramPage() {
  const [diagramContent, setDiagramContent] = useState('');

  useEffect(() => {
    fetch('/large-scale-video-streaming-site.drawio.html')
      .then(response => response.text())
      .then(data => setDiagramContent(data))
      .catch(error => console.error('Error loading diagram:', error));
  }, []);

  return (
    <div>
      <h1>Large Scale Video Streaming Site Diagram</h1>
      <div dangerouslySetInnerHTML={{ __html: diagramContent }} />
      <Link to="/">
        <button>Back to Home</button>
      </Link>
    </div>
  );
}

export default DiagramPage;