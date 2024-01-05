import React, {
  DetailedHTMLProps,
  forwardRef,
  ForwardedRef,
  HTMLAttributes,
} from "react";
import classNames from "classnames";
import { Simulate } from "react-dom/test-utils";
import "./TextArea.css";
import error = Simulate.error;

export interface TextAreaProps
  extends DetailedHTMLProps<
    HTMLAttributes<HTMLTextAreaElement>,
    HTMLTextAreaElement
  > {
  className?: string;
  name?: string;
  type?: string;
  error?: string;
}

export const TextArea = forwardRef(
  (
    { className, name, type, error, ...rest }: TextAreaProps,
    ref: ForwardedRef<HTMLTextAreaElement>,
  ): JSX.Element => {
    return (
      <textarea
        className={classNames(className, "TextArea", {
          TextArea__error: error,
        })}
        name={name}
        ref={ref}
        {...rest}
      />
    );
  },
);

TextArea.displayName = "FormTextArea";
