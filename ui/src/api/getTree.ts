import api from "./base";

export default async function getTreeAPI() {
  const data = await api.get("/file-tree");

  return data.data;
}
