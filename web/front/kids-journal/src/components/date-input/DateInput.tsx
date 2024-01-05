import React, { useRef, useState } from "react";
import { formatDate } from "../../utils/helpers/data";
import { Calendar } from "../calendar/Calendar";
import "./DateInput.css";
import { useClickOutside } from "../../hooks/useClickOutside";

export type DateInputProps = {
  currentData?: Date;
}

export const DateInput = ({ currentData = new Date() }: DateInputProps) => {
  const [selectedDate, setSelectedDay] = useState(currentData);


  const [isOpenCalendar, setOpenCalendar] = useState(false);

  const closeCalendar = () => setOpenCalendar(false);
  const calendarRef = useRef(null);
  useClickOutside(calendarRef, () => {
    if (isOpenCalendar) setTimeout(closeCalendar, 50);
  });

  return (
    <div className="app__container">
      <div
        className="date__container"
        onClick={() => setOpenCalendar(!isOpenCalendar)}
      >
        {formatDate(selectedDate, "DD MMM YYYY")}
      </div>
      <div className={`calendar-move ${isOpenCalendar ? "active" : ""}`}>
        <Calendar
          selectedDate={selectedDate}
          selectDate={(date) => setSelectedDay(date)}
        />
      </div>
    </div>
  );
};
