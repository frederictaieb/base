import React, { useState } from "react";

const AddInnerWeather: React.FC = () => {
  const [form, setForm] = useState({
    lat: "51.5074",
    lng: "-0.1278",
    joy: "1",
    sadness:"2",
    anger:"0",
    fear:"0",
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
      const response = await fetch("http://localhost:8000/add_inner_weather", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
            "point": {
              "lat": parseFloat(form.lat),
              "lng": parseFloat(form.lng)
            },
            "sentences": {
              "sentences": [
                "string"
              ]
            },
            "emotion_score": {
              "joy": form.joy,
              "sadness": form.sadness,
              "anger": form.anger,
              "fear": form.fear
            }
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
        <label>
          Joy:
          <input type="text" name="joy" value={form.joy} onChange={handleChange} required />
        </label>
        <br />
        <label>
          Sadness:
          <input type="text" name="sadness" value={form.sadness} onChange={handleChange} required />
        </label>
        <br />
        <label>
          Anger:
          <input type="text" name="anger" value={form.anger} onChange={handleChange} required />
        </label>
        <br />
        <label>
          Fear:
          <input type="text" name="fear" value={form.fear} onChange={handleChange} required />
        </label>
        <br />
        <label>
          Sentence 1:
          <input type="text" name="sentence_1" value={form.sentence_1} onChange={handleChange} required />
        </label>
        <br />
        <label>
          Sentence 2:
          <input type="text" name="sentence_2" value={form.sentence_2} onChange={handleChange} required />
        </label>
        <br />
        <label>
          Sentence 3:
          <input type="text" name="sentence_3" value={form.sentence_3} onChange={handleChange} required />
        </label>
        <br />
        <button type="submit">Envoyer</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default AddInnerWeather;