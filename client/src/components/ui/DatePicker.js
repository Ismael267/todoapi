"use client"
import React, { useState } from "react";
import { format } from "date-fns";
import { fr } from "date-fns/locale";
import { DayPicker } from "react-day-picker";
import "react-day-picker/dist/style.css";
import { useRouter } from "next/navigation"; 

const css = `
.rdp {
  --rdp-cell-size: 45px;
}
`;

export default function Example() {
  const router = useRouter();
  const [task, setTask] = useState("");
  const [selected, setSelected] = useState(null);
console.log(selected);
  const handleDayClick = (date) => {
    
    setSelected(date);
  };

  console.log(task);
  console.log(selected);

  const addTask = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://127.0.0.1:8000/task/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          task,
          dateOfRealisation: selected.toISOString(),
          completed: false,
          dateOfExecution: selected.toISOString(),
        }),
      });

      if (response.ok) {
        console.log("Réponses ajoutées avec succès");
        location.reload();
      } else {
        console.log(response);
        throw new Error("Erreur pendant l'ajout des réponses.");
      }
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <>
      <style>{css}</style>
      <div className="text-2xl font-semibold">
        <h1>Nouvelle tâche</h1>
      </div>
      <form onSubmit={addTask}>
        <div className="w-full">
          <input
            type="text"
            className="w-full border rounded my-4 py-2 "
            placeholder="  Entrer votre tâche"
            value={task}
            onChange={(e) => setTask(e.target.value)}
            required
          />
        </div>
        <div className="w-fit rounded-lg border font-inter flex justify-around">
          <DayPicker
            mode="single"
            selected={ selected} 
            onDayClick={handleDayClick} 
            locale={fr}
          />
        </div>
        <div className="my-8 flex justify-end">
          <button type="submit" className="bg-blue-500 p-2 px-4 mx-1 rounded-lg text-white">
            Création
          </button>
          <button className="bg-white border p-2 px-4 mx-1 rounded-lg text-gray-500">
            Retour
          </button>
        </div>
      </form>
    </>
  );
}
