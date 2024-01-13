import React from "react";
import { Header } from "../../components/header/Header";
import {AddChild} from "../../components/addChild/AddChild";

type AddChildPageProps = {};

function AddChildPage({}: AddChildPageProps): JSX.Element {
    return (
        <div>
            <Header />
            <AddChild />
        </div>
    );
}

export default AddChildPage;
