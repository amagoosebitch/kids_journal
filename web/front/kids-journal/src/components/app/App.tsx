import React from "react";
import { Button } from "../button/Button";
import { TextArea } from "../textArea/TextArea";

function App() {
  const handleButtonClick = (event: React.MouseEvent) => {
    console.log("[button click event]", event);
  };

  return (
    <div>
      <Button onClick={handleButtonClick}>Кнопка</Button>
      <TextArea>Введите имя</TextArea>
    </div>
  );
}

export default App;
