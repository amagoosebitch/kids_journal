import { useAppSelector } from "../../hooks/useAppDispatch";
import "./ErrorMessage.css";

function ErrorMessage(): JSX.Element | null {
  //const error = useAppSelector((state) => state.error);
  return <div className="error-message">Error</div>;
}

export default ErrorMessage;
