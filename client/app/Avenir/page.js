"use client";

import React, { Fragment, useState, useEffect } from "react";
import Modal from "@/components/ui/Modal";
import { Menu, Transition, Dialog } from "@headlessui/react";
import { format } from "date-fns";
import { fr } from "date-fns/locale";
// import ContextMenu from "@/components/ui/ContextMenu";

import { DayPicker } from "react-day-picker";
const css = `
.rdp {
  --rdp-cell-size: 45px;
}
`; 


export default function Home() {
  const [isChecked, setIsChecked] = useState(false);
  const [selected, setSelected] = useState(null);
  const [tasks, setTasks] = useState([]);

  const fetchTasks = () => {
    fetch("http://127.0.0.1:8000/tasks", {
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        setTasks(data);
        console.log(data.length);
      });
  };
  const hourformat = (dateT) => {
    const Ldate = new Date(dateT);
    return Ldate.toLocaleString("fr-FR", {
      weekday: 'short',
      month: 'short',
      day: 'numeric',
      hour: "numeric",
      minute: "numeric"
    });
  };
  const changeDate = (id) => {
    fetch(`http://127.0.0.1:8000/update/taskDate/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ dateOfRealisation: selected, dateOfExecution:selected }),
    })
    .then(response => {
      if (response.ok) {
        location.reload();
        console.log('Response is OK');
     
      } else {
        console.log('Response is not OK');
      }
    })
    .catch(error => {
      console.error('Error: ', error);
    });;
  };
  const changeDateplus = (id) => {
    fetch(`http://127.0.0.1:8000/update/taskDatePlus/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
    })
    .then(response => {
      if (response.ok) {
        location.reload();
        console.log('Response is OK');
     
      } else {
        console.log('Response is not OK');
      }
    })
    .catch(error => {
      console.error('Error: ', error);
    });;
  };
  const handleDayClick = (date) => {
    const currentDate = format(date, "yyyy-MM-dd", { locale: fr });
    // console.log(currentDate);
    setSelected(currentDate);
  };
  const convertDate = (isoDate) => {
    const date = new Date(isoDate);
    const options = {
      weekday: "short",
      month: "short",
      day: "numeric",
    };
    const formattedDate = date.toLocaleDateString("fr-FR", options);
    return formattedDate;
  };
  let [isOpen1, setIsOpen1] = useState(false);

  function closeModal1() {
    setIsOpen1(false);
  }

  function openModal1() {
    setIsOpen1(true);
  }
  useEffect(() => {
    fetchTasks();
  }, []);
  const toggleCheckbox = (id) => {
    fetch(`http://localhost:8000/update/task/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({ completed: true }),
    })
      .then(response => {
        if (response.ok) {
          location.reload();
          console.log('Response is OK');
       
        } else {
          console.log('Response is not OK');
        }
      })
      .catch(error => {
        console.error('Error: ', error);
      });
  };
  
  const deleteTask = (id) => {
    fetch(`http://localhost:8000/delete/task/${id}`, { 
      headers: {
        "Content-Type":"application/json",
        Accept:"application/json",

      },
      method: "DELETE"

    })
    .then(response => {
      if (response.ok) {
        location.reload();
        console.log('Response is OK');
     
      } else {
        console.log('Response is not OK');
      }
    })
    .catch(error => {
      console.error('Error: ', error);
    });
  };

  // date of today en fr
  const dateT = new Date();
  const dataTY=dateT.toISOString()
  console.log(dataTY);
  // const dateToday=dateT.toLocaleString("fr-Fr",{
  //   weekday: 'long',
  //   month: 'long',
  //   day: 'numeric',
  // })
  // const dateT = new Date();
  const year = dateT.getFullYear();
  const month = String(dateT.getMonth() + 1).padStart(2, "0"); // Mois commence à 0, donc on ajoute 1
  const day = String(dateT.getDate()).padStart(2, "0");
  

  const TodayIsoDate = `${year}-${month}-${day}`;

  // console.log(TodayIsoDate);

  return (
    <>
  
        <div className="text-white mb-8 font-inter ">
          <h1 className="font-semibold text-2xl">À venir</h1>
        </div>
        <div className=" mb-16">
          {tasks.map((task) =>
            !task.completed && task.dateOfRealisation.split('T')[0] > TodayIsoDate ? (
              <div className="bg-gray-100 rounded shadow p-2 mb-3 flex justify-between flex-wrap  max-md:flex-column  ">
                <div className="items-center flex max-md:items-start">
                  <button
                    className="mx-2 rounded-full text-gray-600 max-md:mt-1"
                    // onClick={ () => toggleCheckbox(task.id)}
                  >
                     
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="18"
                        height="18"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="#6F6F70"
                        strokeWidth="2.5"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        className="rounded-lg"
                      >
                        <circle cx="12" cy="12" r="10"></circle>
                      </svg>
                    
                  </button>
                  <label>{task.task}</label>
                </div>
                <div className=" flex items-center ml-auto">
                  <p className="font-light max-md:text-sm">
                    {convertDate(task.dateOfRealisation)}
                  </p>
                  <div className=" text-right">
                    <Menu as="div" className=" inline-block text-left">
                      <div>
                        <Menu.Button className="inline-flex w-full justify-center rounded-md  bg-opacity-20 px py text-sm font-medium text-white hover:bg-opacity-30 focus:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75">
                          <svg
                            fill="#000000"
                            width="15px"
                            height="15px"
                            viewBox="0 0 32 32"
                            version="1.1"
                            xmlns="http://www.w3.org/2000/svg"
                            className="ml-4 max-md:ml-0  hover:bg-gray-200 hover:rounded-full"
                          >
                            <path d="M12.15 28.012v-0.85c0.019-0.069 0.050-0.131 0.063-0.2 0.275-1.788 1.762-3.2 3.506-3.319 1.95-0.137 3.6 0.975 4.137 2.787 0.069 0.238 0.119 0.488 0.181 0.731v0.85c-0.019 0.056-0.050 0.106-0.056 0.169-0.269 1.65-1.456 2.906-3.081 3.262-0.125 0.025-0.25 0.063-0.375 0.094h-0.85c-0.056-0.019-0.113-0.050-0.169-0.056-1.625-0.262-2.862-1.419-3.237-3.025-0.037-0.156-0.081-0.3-0.119-0.444zM20.038 3.988l-0 0.85c-0.019 0.069-0.050 0.131-0.056 0.2-0.281 1.8-1.775 3.206-3.538 3.319-1.944 0.125-3.588-1-4.119-2.819-0.069-0.231-0.119-0.469-0.175-0.7v-0.85c0.019-0.056-0.050-0.106 0.063-0.162 0.3-1.625 1.244-2.688 2.819-3.194 0.206-0.069 0.425-0.106 0.637-0.162h0.85c0.056 0.019 0.113 0.050 0.169 0.056 1.631 0.269 2.863 1.419 3.238 3.025 0.038 0.15 0.075 0.294 0.113 0.437zM20.037 15.575v0.85c-0.019 0.069-0.050 0.131-0.063 0.2-0.281 1.794-1.831 3.238-3.581 3.313-1.969 0.087-3.637-1.1-4.106-2.931-0.050-0.194-0.094-0.387-0.137-0.581v-0.85c0.019-0.069-0.050-0.131 0.063-0.2 0.275-1.794 1.831-3.238 3.581-3.319 1.969-0.094 3.637 1.1 4.106 2.931 0.050 0.2 0.094 0.394 0.137 0.588z"></path>
                          </svg>
                        </Menu.Button>
                      </div>
                      <Transition
                        as={Fragment}
                        enter="transition ease-out duration-100"
                        enterFrom="transform opacity-0 scale-95"
                        enterTo="transform opacity-100 scale-100"
                        leave="transition ease-in duration-75"
                        leaveFrom="transform opacity-100 scale-100"
                        leaveTo="transform opacity-0 scale-95"
                      >
                        <Menu.Items className="fixed mt-2 w-56 origin-top-left right-5 divide-y divide-gray-100 rounded-lg bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                          <div className="px-1 py-1 ">
                            <Menu.Item>
                              {({ active }) => (
                                <button
                                  className={`${
                                    active ? "bg-slate-50 " : "text-gray-900"
                                  } group flex w-full items-center rounded-lg px-2 py-2 text-sm`}
                                  onClick={() => toggleCheckbox(task.id)}
                                >
                                  Marque comme terminé
                                </button>
                              )}
                            </Menu.Item>
                            <Menu.Item>
                              {({ active }) => (
                                <button
                                onClick={()=>changeDateplus(task.id)}
                                  className={`${
                                    active ? "bg-slate-50 " : "text-gray-900"
                                  } group flex w-full items-center rounded-md px-2 py-2 text-sm`}
                                >
                                  Echéance à demain
                                </button>
                              )}
                            </Menu.Item>
                            <Menu.Item>
                              {({ active }) => (
                                <button
                                  className={`${
                                    active ? "bg-slate-50 " : "text-gray-900"
                                  } group flex w-full items-center rounded-md px-2 py-2 text-sm`}
                                  onClick={openModal1}
                                >
                                  Choisir une date
                                </button>
                              )}
                            </Menu.Item>
                          </div>
                          <div className="px-1 py-1">
                            <Menu.Item>
                              {({ active }) => (
                                <button
                                  className={`${
                                    active
                                      ? "bg-slate-50 text-red-600"
                                      :  " text-gray-900"
                                  } group flex w-full items-center rounded-md px-2 py-2 text-sm`}
                                  onClick={() => deleteTask(task.id)}
                                >
                                  Supprimer
                                </button>
                              )}
                            </Menu.Item>
                          </div>
                        </Menu.Items>
                      </Transition>
                    </Menu>
                    <div>
                      <Transition appear show={isOpen1} as={Fragment}>
                        <Dialog
                          as="div"
                          className="relative z-10"
                          onClose={closeModal1}
                        >
                          <Transition.Child
                            as={Fragment}
                            enter="ease-out duration-300"
                            enterFrom="opacity-0"
                            enterTo="opacity-100"
                            leave="ease-in duration-200"
                            leaveFrom="opacity-100"
                            leaveTo="opacity-0"
                          >
                            <div className="fixed inset-0 bg-black bg-opacity-25" />
                          </Transition.Child>
                          <div className="fixed inset-0 overflow-y-auto">
                            <div className="flex min-h-full items-center justify-center p-4 text-center bg-blue-500/10 backdrop-blur-sm">
                              <Transition.Child
                                as={Fragment}
                                enter="ease-out duration-100"
                                enterFrom="opacity-0 scale-95"
                                enterTo="opacity-100 scale-100"
                                leave="ease-in duration-200"
                                leaveFrom="opacity-100 scale-100"
                                leaveTo="opacity-0 scale-95"
                              >
                                <Dialog.Panel className="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle  transition-all m-auto">
                                  <style>{css}</style>
                                  <div className="text-2xl font-semibold mb-4">
                                    <h1>Nouvelle date</h1>
                                  </div>
                                  <form onSubmit={changeDate(task.id)}>
                                    <div className=" rounded-lg border font-inter flex justify-around">
                                      <DayPicker
                                        mode="single"
                                        selected={selected}
                                        onDayClick={handleDayClick}
                                        locale={fr}
                                      />
                                    </div>
                                    <div className="my-4 flex justify-end">
                                      <button
                                        onClick={closeModal1}
                                        className="bg-white border p-2 px-4 mx-1 rounded-lg text-gray-500"
                                      >
                                        Retour
                                      </button>
                                    </div>
                                  </form>
                                </Dialog.Panel>
                              </Transition.Child>
                            </div>
                          </div>
                        </Dialog>
                      </Transition>
                    </div>
                  </div>
                </div>
              </div>
            ) : null
          )}
        </div>
        <div className="">
          <p className="w-fit text-white bg-neutral-900 from-transparent py-1 px-4 rounded text-sm">
            Terminé
          </p>
          <div className="mt-4">
            {tasks.map((task) =>
              task.completed && task.dateOfRealisation.split('T')[0] > TodayIsoDate ? (
                <div className="bg-gray-100 rounded shadow p-2 mb-3 flex justify-between flex-wrap  max-md:flex-column  ">
                  <div className="items-center flex max-md:items-start">
                    <button
                      className="mx-2 rounded-full text-gray-600 max-md:mt-1"
                      onClick={() => toggleCheckbox(task.id)}
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="18"
                        height="18"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="#3366FF"
                        strokeWidth="2.5"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      >
                        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                        <polyline points="22 4 12 14.01 9 11.01"></polyline>
                      </svg>
                    </button>
                    <label className='line-through'>{task.task}</label>
                  </div>
                  <div className="flex items-center ml-auto">
                    <p className="font-light max-md:text-sm">
                      {hourformat(task.updated_at)}
                    </p>
                    <div>
                    <Menu as="div" className=" inline-block text-left">
                      <div>
                        <Menu.Button className="inline-flex w-full justify-center rounded-md  bg-opacity-20 px py text-sm font-medium text-white hover:bg-opacity-30 focus:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75">
                          <svg
                            fill="#000000"
                            width="15px"
                            height="15px"
                            viewBox="0 0 32 32"
                            version="1.1"
                            xmlns="http://www.w3.org/2000/svg"
                            className="ml-4 max-md:ml-0  hover:bg-gray-200 hover:rounded-full"
                          >
                            <path d="M12.15 28.012v-0.85c0.019-0.069 0.050-0.131 0.063-0.2 0.275-1.788 1.762-3.2 3.506-3.319 1.95-0.137 3.6 0.975 4.137 2.787 0.069 0.238 0.119 0.488 0.181 0.731v0.85c-0.019 0.056-0.050 0.106-0.056 0.169-0.269 1.65-1.456 2.906-3.081 3.262-0.125 0.025-0.25 0.063-0.375 0.094h-0.85c-0.056-0.019-0.113-0.050-0.169-0.056-1.625-0.262-2.862-1.419-3.237-3.025-0.037-0.156-0.081-0.3-0.119-0.444zM20.038 3.988l-0 0.85c-0.019 0.069-0.050 0.131-0.056 0.2-0.281 1.8-1.775 3.206-3.538 3.319-1.944 0.125-3.588-1-4.119-2.819-0.069-0.231-0.119-0.469-0.175-0.7v-0.85c0.019-0.056-0.050-0.106 0.063-0.162 0.3-1.625 1.244-2.688 2.819-3.194 0.206-0.069 0.425-0.106 0.637-0.162h0.85c0.056 0.019 0.113 0.050 0.169 0.056 1.631 0.269 2.863 1.419 3.238 3.025 0.038 0.15 0.075 0.294 0.113 0.437zM20.037 15.575v0.85c-0.019 0.069-0.050 0.131-0.063 0.2-0.281 1.794-1.831 3.238-3.581 3.313-1.969 0.087-3.637-1.1-4.106-2.931-0.050-0.194-0.094-0.387-0.137-0.581v-0.85c0.019-0.069-0.050-0.131 0.063-0.2 0.275-1.794 1.831-3.238 3.581-3.319 1.969-0.094 3.637 1.1 4.106 2.931 0.050 0.2 0.094 0.394 0.137 0.588z"></path>
                          </svg>
                        </Menu.Button>
                      </div>
                      <Transition
                        as={Fragment}
                        enter="transition ease-out duration-100"
                        enterFrom="transform opacity-0 scale-95"
                        enterTo="transform opacity-100 scale-100"
                        leave="transition ease-in duration-75"
                        leaveFrom="transform opacity-100 scale-100"
                        leaveTo="transform opacity-0 scale-95"
                      >
                        <Menu.Items className="fixed mt-2 w-56 origin-top-left right-5 divide-y divide-gray-100 rounded-lg bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                          <div className="px-1 py-1 ">
                            <Menu.Item>
                              {({ active }) => (
                                <button
                                  className={`${
                                    active ? "bg-slate-50 " : "text-gray-300"
                                  } group flex w-full items-center rounded-lg px-2 py-2 text-sm`}
                                  onClick={() => toggleCheckbox(task.id)}
                                  disabled
                                >
                                  Marque comme terminé
                                </button>
                              )}
                            </Menu.Item>
                            <Menu.Item>
                              
                              {({ active }) => (
                                <button
                                onClick={()=>changeDateplus(task.id)}
                                  className={`${
                                    active ? "bg-slate-50 " : "text-gray-300"
                                  } group flex w-full items-center rounded-md px-2 py-2 text-sm`}
                                  disabled
                                >
                                  Echéance à demain
                                </button>
                              )}
                            </Menu.Item>
                            <Menu.Item>
                              {({ active }) => (
                                <button
                                  className={`${
                                    active ? "bg-slate-50 " : "text-gray-300"
                                  } group flex w-full items-center rounded-md px-2 py-2 text-sm`}
                                  onClick={openModal1}
                                  disabled
                                >
                                  Choisir une date
                                </button>
                              )}
                            </Menu.Item>
                          </div>
                          <div className="px-1 py-1">
                            <Menu.Item>
                              {({ active }) => (
                                <button
                                  className={`${
                                    active
                                      ? "bg-slate-50 text-red-600"
                                      :  " text-gray-900"
                                  } group flex w-full items-center rounded-md px-2 py-2 text-sm`}
                                  onClick={() => deleteTask(task.id)}
                                >
                                  Supprimer
                                </button>
                              )}
                            </Menu.Item>
                          </div>
                        </Menu.Items>
                      </Transition>
                    </Menu>
                    </div>
                  </div>
                </div>
              ) : null
            )}
          </div>
        </div>
        <div>
          <Modal />
        </div>
     
    </>
  );
}
