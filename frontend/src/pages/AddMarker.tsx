import React, { useState } from "react";
import Drawer from "../components/Drawer";

const AddMarkerDrawer: React.FC<{ isOpen: boolean; onClose: () => void }> = ({ isOpen, onClose }) => {
  const [form, setForm] = useState({
    latitude: "40.7128",
    longitude: "74.0060",
    joy: "1",
    sadness: "2",
    anger: "0",
    fear: "0",
    sentence_1: "test_1",
    sentence_2: "test_2",
    sentence_3: "test_3"
  });
  const [message, setMessage] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage("");
    try {
      const response = await fetch("http://localhost:8000/add_marker", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          location: { latitude: parseFloat(form.latitude), longitude: parseFloat(form.longitude) },
          emotions: {
            joy: parseInt(form.joy),
            sadness: parseInt(form.sadness),
            anger: parseInt(form.anger),
            fear: parseInt(form.fear)
          },
          wisdom: {
            sentence_1: form.sentence_1,
            sentence_2: form.sentence_2,
            sentence_3: form.sentence_3
          }
        }),
      });
      if (!response.ok) throw new Error("Erreur lors de l'envoi du point");
      setMessage("Marker added!");
    } catch (error) {
      setMessage("Erreur : " + error);
    }
  };

  return (
    <Drawer isOpen={isOpen} onClose={onClose}>
      <h2 className="text-2xl font-bold text-center mb-6 text-white">Add Marker</h2>
      <form
        onSubmit={handleSubmit}
        className="grid grid-cols-1 sm:grid-cols-2 gap-4 bg-black p-6 rounded-xl shadow-lg"
      >
        {/* Ligne 1 */}
        <label className="flex flex-col gap-1">
          <span className="text-sm font-medium text-white">Latitude</span>
          <input type="number" step="any" name="latitude" value={form.latitude} onChange={handleChange} required className="block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm text-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-400 focus:outline-none" />
        </label>
        <label className="flex flex-col gap-1">
          <span className="text-sm font-medium text-white">Longitude</span>
          <input type="number" step="any" name="longitude" value={form.longitude} onChange={handleChange} required className="block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm text-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-400 focus:outline-none" />
        </label>
        {/* Ligne 2 */}
        <label className="flex flex-col gap-1">
          <span className="text-sm font-medium text-white">Joy</span>
          <input type="number" name="joy" value={form.joy} onChange={handleChange} required min={0} className="block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm text-gray-300 focus:border-yellow-400 focus:ring-2 focus:ring-yellow-300 focus:outline-none" />
        </label>
        <label className="flex flex-col gap-1">
          <span className="text-sm font-medium text-white">Sadness</span>
          <input type="number" name="sadness" value={form.sadness} onChange={handleChange} required min={0} className="block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm text-gray-300 focus:border-blue-400 focus:ring-2 focus:ring-blue-300 focus:outline-none" />
        </label>
        {/* Ligne 3 */}
        <label className="flex flex-col gap-1">
          <span className="text-sm font-medium text-white">Anger</span>
          <input type="number" name="anger" value={form.anger} onChange={handleChange} required min={0} className="block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm text-gray-300 focus:border-red-400 focus:ring-2 focus:ring-red-300 focus:outline-none" />
        </label>
        <label className="flex flex-col gap-1">
          <span className="text-sm font-medium text-white">Fear</span>
          <input type="number" name="fear" value={form.fear} onChange={handleChange} required min={0} className="block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm text-gray-300 focus:border-green-400 focus:ring-2 focus:ring-green-300 focus:outline-none" />
        </label>
 
        {/* Sentences */}
        <label className="flex flex-col gap-1 sm:col-span-2">
          <span className="text-sm font-medium text-white">Sentence 1</span>
          <input type="text" name="sentence_1" value={form.sentence_1} onChange={handleChange} required className="block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm text-gray-300 focus:border-indigo-400 focus:ring-2 focus:ring-indigo-300 focus:outline-none" />
        </label>
        <label className="flex flex-col gap-1 sm:col-span-2">
          <span className="text-sm font-medium text-white">Sentence 2</span>
          <input type="text" name="sentence_2" value={form.sentence_2} onChange={handleChange} required className="block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm text-gray-300 focus:border-indigo-400 focus:ring-2 focus:ring-indigo-300 focus:outline-none" />
        </label>
        <label className="flex flex-col gap-1 sm:col-span-2">
          <span className="text-sm font-medium text-white">Sentence 3</span>
          <input type="text" name="sentence_3" value={form.sentence_3} onChange={handleChange} required className="block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm text-gray-300 focus:border-indigo-400 focus:ring-2 focus:ring-indigo-300 focus:outline-none" />
        </label>

        <button
        
          type="submit"
          className="sm:col-span-2 w-full py-3 mt-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold text-lg shadow transition-colors duration-200"
        >
          Envoyer
        </button>
        {message && <p className="sm:col-span-2 mt-2 text-center text-sm text-green-600">{message}</p>}
      </form>
    </Drawer>
  );
};

export default AddMarkerDrawer;