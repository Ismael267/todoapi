"use client"

import React, { useState } from "react";
import { format } from "date-fns";
import { fr } from "date-fns/locale";
import { DayPicker } from "react-day-picker";
import "react-day-picker/dist/style.css";

const css = `
.rdp {
  --rdp-cell-size: 45px;
}
`;

export default function Example() {
//   const [task, setTask] = useState(""); 
  const [selected, setSelected] = useState(null);

  const handleDayClick = (date) => {
    const currentDate = format(date, "yyyy-MM-dd", { locale: fr }); 
    // console.log(currentDate);
    setSelected(currentDate); 
  };

// console.log(task)
  const changeDate = (id) => {
   
      fetch(`http://127.0.0.1:8000/update/taskDate/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({dateOfRealisation: selected,dateOfExecution: selected} ), 
      });

      if (response.ok) {
        console.log("date changée avec succès");
      } else {
        console.log(response);
        throw new Error("Erreur ");
      }
  
  };

  return (
    <>
      <style>{css}</style>
      <div className="text-2xl font-semibold">
        <h1>Nouvelle date</h1>
      </div>
      <form onSubmit={changeDate(task.id)}>       
        <div className="w-fit rounded-lg border font-inter flex justify-around">
          <DayPicker
            mode="single"
            selected={new Date(selected)} 
            onDayClick={handleDayClick} 
            locale={fr}
          />
        </div>
        <div className="my-8 flex justify-end">
          <button type="submit" className="bg-blue-500 p-2 px-4 mx-1 rounded-lg text-white">
            Mettre à jour
          </button>
          <button className="bg-white border p-2 px-4 mx-1 rounded-lg text-gray-500">
            Retour
          </button>
        </div>
      </form>
    </>
  );
}
