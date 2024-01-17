import React from "react";
import { Header } from "../../components/header/Header";
import { CreateGroups } from "../../components/createGroups/CreateGroups";
import { useParams } from "react-router-dom";

type CreateGroupsPageProps = {};

function CreateGroupsPage({}: CreateGroupsPageProps): JSX.Element {
  const { organization} = useParams();
    return (
    <div>
      <Header />
      <CreateGroups organization={organization}/>
    </div>
  );
}

export default CreateGroupsPage;
