import React, { useState } from "react";

const TextFormPage: React.FC = () => {
  const [text, setText] = useState("");
  const [submittedText, setSubmittedText] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmittedText(text);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-black p-4">
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow-md w-full max-w-md">
        <label htmlFor="text" className="block mb-2 font-semibold">Saisir du texte :</label>
        <textarea
          id="text"
          value={text}
          onChange={e => setText(e.target.value)}
          className="w-full h-32 p-2 border border-gray-300 rounded mb-4"
          placeholder="Votre texte ici..."
        />
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
        >
          Envoyer
        </button>
      </form>
      {submittedText && (
        <div className="mt-6 bg-white p-4 rounded shadow w-full max-w-md">
          <h2 className="font-bold mb-2">Texte soumis :</h2>
          <p>{submittedText}</p>
        </div>
      )}
    </div>
  );
};

export default TextFormPage; 