import React, { useState } from "react";

const AddPoint: React.FC = () => {
  const [form, setForm] = useState({
    lat: "51.5074",
    lng: "-0.1278",

  });
  const [message, setMessage] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage("");
    try {
      const response = await fetch("http://localhost:8000/add_point", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          lat: parseFloat(form.lat),
          lng: parseFloat(form.lng),
        }),
      });
      if (!response.ok) {
        throw new Error("Erreur lors de l'envoi du point");
      }
      setMessage("Point ajouté avec succès !");
    } catch (error) {
      setMessage("Erreur : " + error);
    }
  };

  return (
    <div>
      <h1 className="text-3xl underline">
        Ajouter un Point
      </h1>
      <form onSubmit={handleSubmit}>
      <label>
          Latitude:
          <input type="text" name="latitude" value={form.lat} onChange={handleChange} required />
        </label>
        <br />
        <label>
          Longitude:
          <input type="text" name="longitude" value={form.lng} onChange={handleChange} required />
        </label>
        <br />
        <button type="submit">Envoyer</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default AddPoint;