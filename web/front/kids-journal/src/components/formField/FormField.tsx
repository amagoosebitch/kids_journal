import React from "react";
import classNames from "classnames";
import "./FormField.css";
import {Input} from "../input/Input";

export type FormFieldType = "text" | "password" | "tel" | "textarea";

export interface FormFieldProps {
  className?: string;
  error?: string;
  label?: string;
  name?: string;
  type: FormFieldType;
  isFocused?: boolean;
  isRequired?: boolean;
  onBlur?: (event: React.FocusEvent<HTMLInputElement>) => void;
  onFocus?: (event: React.FocusEvent<HTMLInputElement>) => void;
}

export const FormField: React.FC<FormFieldProps> = ({
                                                      className,
                                                      error,
                                                      label,
                                                      name,
                                                      type,
                                                      isFocused,
                                                      isRequired,
                                                      onBlur,
                                                      onFocus,
                                                    }: FormFieldProps) => {
  return (
      <div
          className={classNames("FormField", className, {
            FormField__active: isFocused,
          })}
      >
        <label className="FormField-Label" htmlFor={name}>
          {label}
          {isRequired && <span className="FormField-LabelRequired"> *</span>}
        </label>
        {type === "text" && (
            <>
              <Input
                  className={classNames({
                    Input__active: isFocused,
                    Input__error: error,
                  })}
                  name={name}
                  error={error}
                  onBlur={onBlur}
                  onFocus={onFocus}
              />
              {error && <div className="FormField-ErrorMassage">{error}</div>}
            </>
        )}
      </div>
  );
};
