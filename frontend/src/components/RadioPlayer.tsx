import React from 'react';

const RADIO_STREAM_URL = "http://163.172.162.144:8001/eaim";

type RadioPlayerProps = {
  audioRef: React.RefObject<HTMLAudioElement | null>;
};

const RadioPlayer: React.FC<RadioPlayerProps> = ({ audioRef }) => {
  return (
    <audio
      ref={audioRef}
      src={RADIO_STREAM_URL}
      autoPlay
      style={{ display: 'none' }}
    />
  );
};

export default RadioPlayer;
