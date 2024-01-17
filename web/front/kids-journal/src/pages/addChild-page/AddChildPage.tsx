import React from "react";
import { Header } from "../../components/header/Header";
import {AddChild} from "../../components/addChild/AddChild";
import {useParams} from "react-router-dom";

type AddChildPageProps = {};

function AddChildPage({}: AddChildPageProps): JSX.Element {
    const { organization, groupId } = useParams();
    return (
        <div>
            <Header />
            <AddChild organization={organization} groupId={groupId}/>
        </div>
    );
}

export default AddChildPage;
