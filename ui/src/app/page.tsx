"use client";

import ViewVideo from "@/component/ViewVideo";
import useGetTree from "@/queries/useGetTree";
import {
  CalendarOutlined,
  FolderOutlined,
  PlaySquareOutlined,
} from "@ant-design/icons";
import { DatePicker, Tree } from "antd";
import dayjs from "dayjs";
import React from "react";

export default function Home() {
  const { data } = useGetTree();
  const [selectedKeys, setSelectedKeys] = React.useState<string>("");

  const [dateRange, setDateRange] = React.useState<string[]>([]);

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const transformToTreeData = (data: any) => {
    return Object?.keys(data)
      .map((date) => {
        return {
          title: date,
          selectable: false,
          key: date,
          icon: <CalendarOutlined />,
          children: Object.keys(data[date]).map((category) => ({
            title: category,
            icon: <FolderOutlined />,
            selectable: false,
            key: `${date}/${category}`,
            children: Object.keys(data[date][category]).map((file) => ({
              title: file.replace(".mp4", "").slice(-8),
              key: `${date}/${category}/${file}`,
              icon: <PlaySquareOutlined />,
              selectable: true,
            })),
          })),
        };
      })
      .sort((a, b) => {
        return a.key.localeCompare(b.key) * -1;
      });
  };

  const dataTree = React.useMemo(() => {
    if (!data) {
      return [];
    }

    const covertedData = transformToTreeData(data);

    if (dateRange.length === 0) {
      return covertedData;
    }

    const [start, end] = dateRange;

    const filteredData = covertedData.filter((date) => {
      if (
        dayjs(date.key).isBefore(dayjs(start)) ||
        dayjs(date.key).isAfter(dayjs(end))
      ) {
        return false;
      }

      return true;
    });

    return filteredData;
  }, [data, dateRange]);

  return (
    <div className="flex h-screen w-screen flex-row gap-4 p-8">
      <div className="w-1/6 border-r-2 border-gray-200 flex flex-col gap-4">
        <div>
          <DatePicker.RangePicker
            onChange={(_, dateString) => {
              setDateRange(dateString);
            }}
          />
        </div>
        <div className="my-auto h-full overflow-auto">
          <Tree
            showLine
            showIcon
            treeData={dataTree}
            onSelect={(selectedKeys) => {
              setSelectedKeys(selectedKeys[0] as string);
            }}
            multiple={false}
            defaultExpandAll
          />
        </div>
      </div>
      <div className="w-5/6">
        <ViewVideo videoKey={selectedKeys} />
      </div>
    </div>
  );
}
