"use client"

import React, { useState } from "react";
import "react-modern-calendar-datepicker/lib/DatePicker.css";
import { Calendar, utils } from "react-modern-calendar-datepicker";

const myCustomLocale = {
  months: [
    'Janvier',
    'Fevrier',
    'Mars',
    'Avril',
    'Mai',
    'Juin',
    'Juillet',
    'Août',
    'Septembre',
    'Octobre',
    'Novembre',
    'Decembre',
  ],
  weekDays: [
    {
      name: 'Dimanche',
      short: 'Di',
      isWeekend: true,
    },
    {
      name: 'Lundi',
      short: 'Lu',
    },
    {
      name: 'Mardi',
      short: 'Ma',
    },
    {
      name: 'Mercredi',
      short: 'Me',
    },
    {
      name: 'Jeudi',
      short: 'Je',
    },
    {
      name: 'Vendredi',
      short: 'Ve',
    },
    {
      name: 'Samedi',
      short: 'Sa',
      isWeekend: true,
    },
  ],
  weekStartingIndex: 0,
  getToday(gregorianTodayObject) {
    return gregorianTodayObject;
  },
  toNativeDate(date) {
    return new Date(date.year, date.month - 1, date.day);
  },
  getMonthLength(date) {
    return new Date(date.year, date.month, 0).getDate();
  },
  transformDigit(digit) {
    return digit;
  },
  nextMonth: 'Next Month',
  previousMonth: 'Previous Month',
  openMonthSelector: 'Open Month Selector',
  openYearSelector: 'Open Year Selector',
  closeMonthSelector: 'Close Month Selector',
  closeYearSelector: 'Close Year Selector',
  defaultPlaceholder: 'Select...',
  from: 'from',
  to: 'to',
  digitSeparator: ',',
  yearLetterSkip: 0,
  isRtl: false,
};

const Page = () => {
  const [selectedDay, setSelectedDay] = useState(null);

  const handleDateChange = (date) => {
    // setSelectedDay(date);
    const formattedDate = `${date.year}-${String(date.month).padStart(2, '0')}-${String(date.day).padStart(2, '0')}`;
    setSelectedDay(formattedDate);
  };

  console.log(JSON.stringify(selectedDay));

  return (
    <div className="m-auto">
      <Calendar
        // value={selectedDay}
        onChange={handleDateChange}
        minimumDate={utils().getToday()}
        locale={myCustomLocale}
        colorPrimary="#9c88ff"
        calendarClassName="custom-calendar"
        calendarTodayClassName="custom-today-day"
      />
    </div>
  );
};

export default Page;
