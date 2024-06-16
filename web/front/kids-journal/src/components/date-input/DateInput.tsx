import React, { useRef, useState } from "react";
import { formatDate } from "../../utils/helpers/data";
import { Calendar } from "../calendar/Calendar";
import "./DateInput.css";
import { useClickOutside } from "../../hooks/useClickOutside";
import { Link } from "react-router-dom";
import { AppRoute } from "../../const";

export type DateInputProps = {
  currentData?: Date;
  organization: string | undefined;
  getDate: (date: Date) => void;
};

export const DateInput = ({
  currentData = new Date(),
  organization,
  getDate,
}: DateInputProps) => {
  const [selectedDate, setSelectedDay] = useState(currentData);

  const [isOpenCalendar, setOpenCalendar] = useState(false);

  const closeCalendar = () => setOpenCalendar(false);
  const calendarRef = useRef(null);
  useClickOutside(calendarRef, () => {
    if (isOpenCalendar) setTimeout(closeCalendar, 50);
  });

  function handleCalendar(date: Date) {
    getDate(date);
    setSelectedDay(date);
  }

  return (
    <div className="app__container">
      <div
        className="date__container"
        onClick={() => setOpenCalendar(!isOpenCalendar)}
      >
        <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="6" y="7" width="36" height="36" rx="10" stroke="black" stroke-width="3"/>
          <path d="M6 17H42" stroke="black" stroke-width="3" stroke-linejoin="round"/>
          <path d="M33 4L33 10" stroke="black" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M15 4L15 10" stroke="black" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M13 25H15" stroke="black" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M23 25H25" stroke="black" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M33 25H35" stroke="black" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M13 33H15" stroke="black" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M23 33H25" stroke="black" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M33 33H35" stroke="black" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>

        {formatDate(selectedDate, "DDDD, DD MMM")}
      </div>
      <div className={`calendar-move ${isOpenCalendar ? "active" : ""}`}>
        <Calendar
          selectedDate={selectedDate}
          selectDate={(date) => handleCalendar(date)}
        />
      </div>
    </div>
  );
};
