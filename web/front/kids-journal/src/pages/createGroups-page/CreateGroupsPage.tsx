import React from "react";
import { Header } from "../../components/header/Header";
import { CreateGroups } from "../../components/createGroups/CreateGroups";
import { useParams } from "react-router-dom";

type CreateGroupsPageProps = {};

function CreateGroupsPage({}: CreateGroupsPageProps): JSX.Element {
  return (
    <div>
      <Header />
      <CreateGroups />
    </div>
  );
}

export default CreateGroupsPage;
