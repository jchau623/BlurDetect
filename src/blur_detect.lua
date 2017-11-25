--[[
	For initial purposes, we'll read in a folder of images and 
	process these ones
--]]

local lfs = require('lfs')

--[[
	Function modified from attrdir in:
	https://keplerproject.github.io/luafilesystem/examples.html

	TODO: ensure it's a RAW file... but how? Not a standardized format...
	TODO: what about recursive folder entries?
--]]
function readImage(path)
	os.execute("python read_raws.py " .. path)
end

function getImages (path)
    for file in lfs.dir(path) do
        if file ~= "." and file ~= ".." then
            local f = path..'/'..file
            local attr = lfs.attributes (f)
            assert (type(attr) == "table")
            if attr.mode == "directory" then
                getImages (f)
            else 
	            readImage(f)
            end
        end
    end
end

getImages(arg[1])
--[[

--]]
